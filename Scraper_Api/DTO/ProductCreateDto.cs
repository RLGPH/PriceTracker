namespace Scraper_Api.DTO
{
    public class ProductCreateDto
    {
        public string VendorName { get; set; } = string.Empty;
        public string ProduktName { get; set; } = string.Empty;
        public string? VendorUrl { get; set; }
    }
}
