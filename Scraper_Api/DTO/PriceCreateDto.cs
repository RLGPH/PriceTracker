namespace Scraper_Api.DTO
{
    public class PriceCreateDto
    {
        public int ProductID { get; set; }
        public decimal Price { get; set; }
        public DateTime RetrievalDateTime { get; set; }
    }

}
