namespace Scraper_Api.DTO
{
    public class ProductWithPriceDto
    {
        public ProductCreateDto Product { get; set; } = new();
        public PriceCreateDto Price { get; set; } = new();
    }
}
