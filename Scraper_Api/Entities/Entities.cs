namespace Scraper_Api.Entities
{
    public class Product
    {
        public int ID { get; set; }
        public string VendorName { get; set; } = string.Empty;
        public string ProduktName { get; set; } = string.Empty;
        public string? VendorUrl { get; set; }

        public List<PriceHistory> PriceHistory { get; set; } = new();
    }

    public class PriceHistory
    {
        public int ID { get; set; }
        public int ProductID { get; set; }
        public Product Product { get; set; } = null!;
        public decimal Price { get; set; }
        public DateTime RetrievalDateTime { get; set; } = DateTime.UtcNow;
    }
}
