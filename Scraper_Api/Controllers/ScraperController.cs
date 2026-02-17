using AutoMapper;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Scraper_Api.Data;
using Scraper_Api.DTO;
using Scraper_Api.Entities;

namespace Scraper_Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ScraperController : ControllerBase
    {
        private readonly AppDbContext _context;
        private readonly IMapper _mapper;

        public ScraperController(AppDbContext context, IMapper mapper)
        {
            _context = context;
            _mapper = mapper;
        }

        /// <summary>
        /// POST: api/scraper
        /// Adds a product and/or price history.
        /// </summary>
        [HttpPost]
        public async Task<ActionResult> PostProductWithPrice([FromBody] ProductWithPriceDto dto)
        {
            var productDto = dto.Product;
            var priceDto = dto.Price;

            // Try to find exact existing product
            var existingProduct = await _context.Products
                .Include(p => p.PriceHistory)
                .FirstOrDefaultAsync(p =>
                    p.VendorName == productDto.VendorName &&
                    p.ProduktName == productDto.ProduktName &&
                    p.VendorUrl == productDto.VendorUrl);

            Product product;
            if (existingProduct != null)
            {
                product = existingProduct;
            }
            else
            {
                // Create new product
                product = _mapper.Map<Product>(productDto);
                _context.Products.Add(product);
                await _context.SaveChangesAsync();
            }

            // Add price history
            var priceHistory = new PriceHistory
            {
                ProductID = product.ID,
                Price = priceDto.Price,
                RetrievalDateTime = DateTime.UtcNow // override
            };

            _context.PriceHistories.Add(priceHistory);
            await _context.SaveChangesAsync();

            return Ok(new
            {
                ProductID = product.ID,
                PriceID = priceHistory.ID
            });
        }

        /// <summary>
        /// DELETE: api/scraper/{id}
        /// Deletes a product and all related price history.
        /// </summary>
        [HttpDelete("{id:int}")]
        public async Task<ActionResult> DeleteProduct(int id)
        {
            var product = await _context.Products
                .Include(p => p.PriceHistory)
                .FirstOrDefaultAsync(p => p.ID == id);

            if (product == null) return NotFound();

            _context.Products.Remove(product);
            await _context.SaveChangesAsync();

            return NoContent();
        }
    }
}
