using AutoMapper;
using Scraper_Api.DTO;
using Scraper_Api.Entities;


namespace Scraper_Api.Mapping
{
    public class MappingProfile : Profile
    {
        public MappingProfile()
        {
            CreateMap<ProductCreateDto, Product>();
            CreateMap<Product, ProductReadDto>();

            CreateMap<PriceCreateDto, PriceHistory>()
                .ForMember(dest => dest.RetrievalDateTime,
                           opt => opt.MapFrom(src => src.RetrievalDateTime));

            CreateMap<PriceHistory, PriceReadDto>();
        }
    }
}
