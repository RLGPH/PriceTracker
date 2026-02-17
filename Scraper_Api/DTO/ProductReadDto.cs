namespace Scraper_Api.DTO
{
    public class ProductReadDto
    {
        public int ID { get; set; }
        public string VendorName { get; set; } = string.Empty;
        public string ProduktName { get; set; } = string.Empty;
        public string? VendorUrl { get; set; }

        public List<PriceReadDto>? PriceHistory { get; set; }
    }

}
