from hashlib import md5
import re
from sqlalchemy import Boolean, Column, Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class StatusEnum(enum.Enum):
    on_sale = 1
    pending = 2
    sold = 3


class TransmissionEnum(enum.Enum):
    manual = 1
    automatic = 2
    unknown = 3


class Car(Base):
    __tablename__ = "cars"
    sale_id = Column(Integer, primary_key=True)
    model = Column(String)
    brand = Column(String)
    year = Column(Integer)
    price = Column(Float)
    status = Column(Enum(StatusEnum))
    miles = Column(Integer, nullable=True)
    transmission = Column(Enum(TransmissionEnum), nullable=True)
    featured = Column(Boolean, nullable=True, default=False)
    inspected = Column(Boolean, nullable=True, default=False)
    location = Column(String, nullable=True)
    reserve = Column(Boolean, nullable=True)
    url = Column(String)
    image_url = Column(String)
    end_date = Column(String)
    horsepower = Column(String, nullable=True)
    modifications = Column(String, nullable=True)
    ownership = Column(String, nullable=True)
    extra = Column(String, nullable=True)

    def __repr__(self):
        return f"<Car(brand='{self.brand}', model='{self.model}', year={self.year}, price={self.price})>"

    def to_dict(self):
        return {
            "sale_id": self.sale_id,
            "model": self.model,
            "brand": self.brand,
            "year": self.year,
            "price": float(self.price) if self.price else None,
            "status": self.status.value if self.status else None,
            "miles": self.miles,
            "transmission": self.transmission.value if self.transmission else None,
            "featured": self.featured,
            "inspected": self.inspected,
            "location": self.location,
            "reserve": self.reserve,
            "url": self.url,
            "image_url": self.image_url,
            "end_date": self.end_date,
            "horsepower": self.horsepower,
            "modifications": self.modifications,
            "ownership": self.ownership,
            "extra": self.extra,
        }

    @staticmethod
    def generate_id(url):
        return int(
            md5(re.sub(r"[^a-zA-Z0-9]", "", url).lower().encode("utf-8")).hexdigest(),
            16,
        ) % ((1 << 31) - 1)

    @staticmethod
    def parse_trans(t):
        transmission_enum_value = None

        if t == "Unknown" or t == None:
            transmission_enum_value = TransmissionEnum.unknown
        elif t.startswith("Automatic"):
            transmission_enum_value = TransmissionEnum.automatic
        else:
            transmission_enum_value = TransmissionEnum.manual
        return transmission_enum_value

    @staticmethod
    def extract_car_details(title: str):
        parts = title.split()
        if len(parts) > 1:
            year = int(parts[0])
            brand_model = " ".join(parts[1:])
            model_parts = brand_model.split(" ")
            return {"year": year, "brand": model_parts[0], "model": " ".join(model_parts[1:])}
        
    @staticmethod    
    def parse_mileage(miles):
        if miles is not None:
            match = re.match(r"~?(\d{1,3}(?:,\d{3})*)", miles)
            if match:
                return int(match.group(1).replace(",", ""))
        return None
