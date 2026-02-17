using Microsoft.EntityFrameworkCore;
using Scraper_Api.Entities;

namespace Scraper_Api.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options)
            : base(options) { }

        public DbSet<Product> Products => Set<Product>();
        public DbSet<PriceHistory> PriceHistories => Set<PriceHistory>();

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<PriceHistory>()
                .HasOne(p => p.Product)
                .WithMany(p => p.PriceHistory)
                .HasForeignKey(p => p.ProductID)
                .OnDelete(DeleteBehavior.Cascade);
        }
    }
}
