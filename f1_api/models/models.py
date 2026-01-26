from typing import Optional
import datetime
import decimal

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKeyConstraint,
    Index,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Continent(Base):
    __tablename__ = "continent"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="continent_pkey"),
        UniqueConstraint("code", name="continent_code_key"),
        UniqueConstraint("name", name="continent_name_key"),
    )

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    code: Mapped[str] = mapped_column(String(2), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    demonym: Mapped[str] = mapped_column(String(100), nullable=False)

    country: Mapped[list["Country"]] = relationship("Country", back_populates="continent")


t_driver_of_the_day_result = Table(
    "driver_of_the_day_result",
    Base.metadata,
    Column("race_id", Integer),
    Column("position_display_order", Integer),
    Column("position_number", Integer),
    Column("position_text", String(4)),
    Column("driver_number", String(3)),
    Column("driver_id", String(100)),
    Column("constructor_id", String(100)),
    Column("engine_manufacturer_id", String(100)),
    Column("tyre_manufacturer_id", String(100)),
    Column("percentage", Numeric(4, 1)),
)


class Entrant(Base):
    __tablename__ = "entrant"
    __table_args__ = (PrimaryKeyConstraint("id", name="entrant_pkey"), Index("entr_name_idx", "name"))

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    season_entrant: Mapped[list["SeasonEntrant"]] = relationship("SeasonEntrant", back_populates="entrant")
    season_entrant_constructor: Mapped[list["SeasonEntrantConstructor"]] = relationship(
        "SeasonEntrantConstructor", back_populates="entrant"
    )
    season_entrant_driver: Mapped[list["SeasonEntrantDriver"]] = relationship(
        "SeasonEntrantDriver", back_populates="entrant"
    )
    season_entrant_tyre_manufacturer: Mapped[list["SeasonEntrantTyreManufacturer"]] = relationship(
        "SeasonEntrantTyreManufacturer", back_populates="entrant"
    )
    season_entrant_chassis: Mapped[list["SeasonEntrantChassis"]] = relationship(
        "SeasonEntrantChassis", back_populates="entrant"
    )
    season_entrant_engine: Mapped[list["SeasonEntrantEngine"]] = relationship(
        "SeasonEntrantEngine", back_populates="entrant"
    )


t_fastest_lap = Table(
    "fastest_lap",
    Base.metadata,
    Column("race_id", Integer),
    Column("position_display_order", Integer),
    Column("position_number", Integer),
    Column("position_text", String(4)),
    Column("driver_number", String(3)),
    Column("driver_id", String(100)),
    Column("constructor_id", String(100)),
    Column("engine_manufacturer_id", String(100)),
    Column("tyre_manufacturer_id", String(100)),
    Column("lap", Integer),
    Column("time", String(20)),
    Column("time_millis", Integer),
    Column("gap", String(20)),
    Column("gap_millis", Integer),
    Column("interval", String(20)),
    Column("interval_millis", Integer),
)


t_free_practice_1_result = Table(
    "free_practice_1_result",
    Base.metadata,
    Column("race_id", Integer),
    Column("position_display_order", Integer),
    Column("position_number", Integer),
    Column("position_text", String(4)),
    Column("driver_number", String(3)),
    Column("driver_id", String(100)),
    Column("constructor_id", String(100)),
    Column("engine_manufacturer_id", String(100)),
    Column("tyre_manufacturer_id", String(100)),
    Column("time", String(20)),
    Column("time_millis", Integer),
    Column("gap", String(20)),
    Column("gap_millis", Integer),
    Column("interval", String(20)),
    Column("interval_millis", Integer),
    Column("laps", Integer),
)


t_free_practice_2_result = Table(
    "free_practice_2_result",
    Base.metadata,
    Column("race_id", Integer),
    Column("position_display_order", Integer),
    Column("position_number", Integer),
    Column("position_text", String(4)),
    Column("driver_number", String(3)),
    Column("driver_id", String(100)),
    Column("constructor_id", String(100)),
    Column("engine_manufacturer_id", String(100)),
    Column("tyre_manufacturer_id", String(100)),
    Column("time", String(20)),
    Column("time_millis", Integer),
    Column("gap", String(20)),
    Column("gap_millis", Integer),
    Column("interval", String(20)),
    Column("interval_millis", Integer),
    Column("laps", Integer),
)


t_free_practice_3_result = Table(
    "free_practice_3_result",
    Base.metadata,
    Column("race_id", Integer),
    Column("position_display_order", Integer),
    Column("position_number", Integer),
    Column("position_text", String(4)),
    Column("driver_number", String(3)),
    Column("driver_id", String(100)),
    Column("constructor_id", String(100)),
    Column("engine_manufacturer_id", String(100)),
    Column("tyre_manufacturer_id", String(100)),
    Column("time", String(20)),
    Column("time_millis", Integer),
    Column("gap", String(20)),
    Column("gap_millis", Integer),
    Column("interval", String(20)),
    Column("interval_millis", Integer),
    Column("laps", Integer),
)


t_free_practice_4_result = Table(
    "free_practice_4_result",
    Base.metadata,
    Column("race_id", Integer),
    Column("position_display_order", Integer),
    Column("position_number", Integer),
    Column("position_text", String(4)),
    Column("driver_number", String(3)),
    Column("driver_id", String(100)),
    Column("constructor_id", String(100)),
    Column("engine_manufacturer_id", String(100)),
    Column("tyre_manufacturer_id", String(100)),
    Column("time", String(20)),
    Column("time_millis", Integer),
    Column("gap", String(20)),
    Column("gap_millis", Integer),
    Column("interval", String(20)),
    Column("interval_millis", Integer),
    Column("laps", Integer),
)


t_pit_stop = Table(
    "pit_stop",
    Base.metadata,
    Column("race_id", Integer),
    Column("position_display_order", Integer),
    Column("position_number", Integer),
    Column("position_text", String(4)),
    Column("driver_number", String(3)),
    Column("driver_id", String(100)),
    Column("constructor_id", String(100)),
    Column("engine_manufacturer_id", String(100)),
    Column("tyre_manufacturer_id", String(100)),
    Column("stop", Integer),
    Column("lap", Integer),
    Column("time", String(20)),
    Column("time_millis", Integer),
)


t_pre_qualifying_result = Table(
    "pre_qualifying_result",
    Base.metadata,
    Column("race_id", Integer),
    Column("position_display_order", Integer),
    Column("position_number", Integer),
    Column("position_text", String(4)),
    Column("driver_number", String(3)),
    Column("driver_id", String(100)),
    Column("constructor_id", String(100)),
    Column("engine_manufacturer_id", String(100)),
    Column("tyre_manufacturer_id", String(100)),
    Column("time", String(20)),
    Column("time_millis", Integer),
    Column("gap", String(20)),
    Column("gap_millis", Integer),
    Column("interval", String(20)),
    Column("interval_millis", Integer),
    Column("laps", Integer),
)


t_qualifying_1_result = Table(
    "qualifying_1_result",
    Base.metadata,
    Column("race_id", Integer),
    Column("position_display_order", Integer),
    Column("position_number", Integer),
    Column("position_text", String(4)),
    Column("driver_number", String(3)),
    Column("driver_id", String(100)),
    Column("constructor_id", String(100)),
    Column("engine_manufacturer_id", String(100)),
    Column("tyre_manufacturer_id", String(100)),
    Column("time", String(20)),
    Column("time_millis", Integer),
    Column("gap", String(20)),
    Column("gap_millis", Integer),
    Column("interval", String(20)),
    Column("interval_millis", Integer),
    Column("laps", Integer),
)


t_qualifying_2_result = Table(
    "qualifying_2_result",
    Base.metadata,
    Column("race_id", Integer),
    Column("position_display_order", Integer),
    Column("position_number", Integer),
    Column("position_text", String(4)),
    Column("driver_number", String(3)),
    Column("driver_id", String(100)),
    Column("constructor_id", String(100)),
    Column("engine_manufacturer_id", String(100)),
    Column("tyre_manufacturer_id", String(100)),
    Column("time", String(20)),
    Column("time_millis", Integer),
    Column("gap", String(20)),
    Column("gap_millis", Integer),
    Column("interval", String(20)),
    Column("interval_millis", Integer),
    Column("laps", Integer),
)


t_qualifying_result = Table(
    "qualifying_result",
    Base.metadata,
    Column("race_id", Integer),
    Column("position_display_order", Integer),
    Column("position_number", Integer),
    Column("position_text", String(4)),
    Column("driver_number", String(3)),
    Column("driver_id", String(100)),
    Column("constructor_id", String(100)),
    Column("engine_manufacturer_id", String(100)),
    Column("tyre_manufacturer_id", String(100)),
    Column("time", String(20)),
    Column("time_millis", Integer),
    Column("q1", String(20)),
    Column("q1_millis", Integer),
    Column("q2", String(20)),
    Column("q2_millis", Integer),
    Column("q3", String(20)),
    Column("q3_millis", Integer),
    Column("gap", String(20)),
    Column("gap_millis", Integer),
    Column("interval", String(20)),
    Column("interval_millis", Integer),
    Column("laps", Integer),
)


t_race_result = Table(
    "race_result",
    Base.metadata,
    Column("race_id", Integer),
    Column("position_display_order", Integer),
    Column("position_number", Integer),
    Column("position_text", String(4)),
    Column("driver_number", String(3)),
    Column("driver_id", String(100)),
    Column("constructor_id", String(100)),
    Column("engine_manufacturer_id", String(100)),
    Column("tyre_manufacturer_id", String(100)),
    Column("shared_car", Boolean),
    Column("laps", Integer),
    Column("time", String(20)),
    Column("time_millis", Integer),
    Column("time_penalty", String(20)),
    Column("time_penalty_millis", Integer),
    Column("gap", String(20)),
    Column("gap_millis", Integer),
    Column("gap_laps", Integer),
    Column("interval", String(20)),
    Column("interval_millis", Integer),
    Column("reason_retired", String(100)),
    Column("points", Numeric(8, 2)),
    Column("pole_position", Boolean),
    Column("qualification_position_number", Integer),
    Column("qualification_position_text", String(4)),
    Column("grid_position_number", Integer),
    Column("grid_position_text", String(2)),
    Column("positions_gained", Integer),
    Column("pit_stops", Integer),
    Column("fastest_lap", Boolean),
    Column("driver_of_the_day", Boolean),
    Column("grand_slam", Boolean),
)


class Season(Base):
    __tablename__ = "season"
    __table_args__ = (PrimaryKeyConstraint("year", name="season_pkey"),)

    year: Mapped[int] = mapped_column(Integer, primary_key=True)

    season_entrant: Mapped[list["SeasonEntrant"]] = relationship("SeasonEntrant", back_populates="season")
    race: Mapped[list["Race"]] = relationship("Race", back_populates="season")
    season_constructor: Mapped[list["SeasonConstructor"]] = relationship("SeasonConstructor", back_populates="season")
    season_constructor_standing: Mapped[list["SeasonConstructorStanding"]] = relationship(
        "SeasonConstructorStanding", back_populates="season"
    )
    season_driver: Mapped[list["SeasonDriver"]] = relationship("SeasonDriver", back_populates="season")
    season_driver_standing: Mapped[list["SeasonDriverStanding"]] = relationship(
        "SeasonDriverStanding", back_populates="season"
    )
    season_engine_manufacturer: Mapped[list["SeasonEngineManufacturer"]] = relationship(
        "SeasonEngineManufacturer", back_populates="season"
    )
    season_entrant_constructor: Mapped[list["SeasonEntrantConstructor"]] = relationship(
        "SeasonEntrantConstructor", back_populates="season"
    )
    season_entrant_driver: Mapped[list["SeasonEntrantDriver"]] = relationship(
        "SeasonEntrantDriver", back_populates="season"
    )
    season_entrant_tyre_manufacturer: Mapped[list["SeasonEntrantTyreManufacturer"]] = relationship(
        "SeasonEntrantTyreManufacturer", back_populates="season"
    )
    season_tyre_manufacturer: Mapped[list["SeasonTyreManufacturer"]] = relationship(
        "SeasonTyreManufacturer", back_populates="season"
    )
    season_entrant_chassis: Mapped[list["SeasonEntrantChassis"]] = relationship(
        "SeasonEntrantChassis", back_populates="season"
    )
    season_entrant_engine: Mapped[list["SeasonEntrantEngine"]] = relationship(
        "SeasonEntrantEngine", back_populates="season"
    )


t_sprint_qualifying_result = Table(
    "sprint_qualifying_result",
    Base.metadata,
    Column("race_id", Integer),
    Column("position_display_order", Integer),
    Column("position_number", Integer),
    Column("position_text", String(4)),
    Column("driver_number", String(3)),
    Column("driver_id", String(100)),
    Column("constructor_id", String(100)),
    Column("engine_manufacturer_id", String(100)),
    Column("tyre_manufacturer_id", String(100)),
    Column("time", String(20)),
    Column("time_millis", Integer),
    Column("q1", String(20)),
    Column("q1_millis", Integer),
    Column("q2", String(20)),
    Column("q2_millis", Integer),
    Column("q3", String(20)),
    Column("q3_millis", Integer),
    Column("gap", String(20)),
    Column("gap_millis", Integer),
    Column("interval", String(20)),
    Column("interval_millis", Integer),
    Column("laps", Integer),
)


t_sprint_race_result = Table(
    "sprint_race_result",
    Base.metadata,
    Column("race_id", Integer),
    Column("position_display_order", Integer),
    Column("position_number", Integer),
    Column("position_text", String(4)),
    Column("driver_number", String(3)),
    Column("driver_id", String(100)),
    Column("constructor_id", String(100)),
    Column("engine_manufacturer_id", String(100)),
    Column("tyre_manufacturer_id", String(100)),
    Column("laps", Integer),
    Column("time", String(20)),
    Column("time_millis", Integer),
    Column("time_penalty", String(20)),
    Column("time_penalty_millis", Integer),
    Column("gap", String(20)),
    Column("gap_millis", Integer),
    Column("gap_laps", Integer),
    Column("interval", String(20)),
    Column("interval_millis", Integer),
    Column("reason_retired", String(100)),
    Column("points", Numeric(8, 2)),
    Column("qualification_position_number", Integer),
    Column("qualification_position_text", String(4)),
    Column("grid_position_number", Integer),
    Column("grid_position_text", String(2)),
    Column("positions_gained", Integer),
)


t_sprint_starting_grid_position = Table(
    "sprint_starting_grid_position",
    Base.metadata,
    Column("race_id", Integer),
    Column("position_display_order", Integer),
    Column("position_number", Integer),
    Column("position_text", String(4)),
    Column("driver_number", String(3)),
    Column("driver_id", String(100)),
    Column("constructor_id", String(100)),
    Column("engine_manufacturer_id", String(100)),
    Column("tyre_manufacturer_id", String(100)),
    Column("qualification_position_number", Integer),
    Column("qualification_position_text", String(4)),
    Column("grid_penalty", String(20)),
    Column("grid_penalty_positions", Integer),
    Column("time", String(20)),
    Column("time_millis", Integer),
)


t_starting_grid_position = Table(
    "starting_grid_position",
    Base.metadata,
    Column("race_id", Integer),
    Column("position_display_order", Integer),
    Column("position_number", Integer),
    Column("position_text", String(4)),
    Column("driver_number", String(3)),
    Column("driver_id", String(100)),
    Column("constructor_id", String(100)),
    Column("engine_manufacturer_id", String(100)),
    Column("tyre_manufacturer_id", String(100)),
    Column("qualification_position_number", Integer),
    Column("qualification_position_text", String(4)),
    Column("grid_penalty", String(20)),
    Column("grid_penalty_positions", Integer),
    Column("time", String(20)),
    Column("time_millis", Integer),
)


t_warming_up_result = Table(
    "warming_up_result",
    Base.metadata,
    Column("race_id", Integer),
    Column("position_display_order", Integer),
    Column("position_number", Integer),
    Column("position_text", String(4)),
    Column("driver_number", String(3)),
    Column("driver_id", String(100)),
    Column("constructor_id", String(100)),
    Column("engine_manufacturer_id", String(100)),
    Column("tyre_manufacturer_id", String(100)),
    Column("time", String(20)),
    Column("time_millis", Integer),
    Column("gap", String(20)),
    Column("gap_millis", Integer),
    Column("interval", String(20)),
    Column("interval_millis", Integer),
    Column("laps", Integer),
)


class Country(Base):
    __tablename__ = "country"
    __table_args__ = (
        ForeignKeyConstraint(["continent_id"], ["continent.id"], name="country_continent_id_fkey"),
        PrimaryKeyConstraint("id", name="country_pkey"),
        UniqueConstraint("alpha2_code", name="country_alpha2_code_key"),
        UniqueConstraint("alpha3_code", name="country_alpha3_code_key"),
        UniqueConstraint("name", name="country_name_key"),
        Index("cntr_continent_id_idx", "continent_id"),
    )

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    alpha2_code: Mapped[str] = mapped_column(String(2), nullable=False)
    alpha3_code: Mapped[str] = mapped_column(String(3), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    continent_id: Mapped[str] = mapped_column(String(100), nullable=False)
    ioc_code: Mapped[Optional[str]] = mapped_column(String(3))
    demonym: Mapped[Optional[str]] = mapped_column(String(100))

    continent: Mapped["Continent"] = relationship("Continent", back_populates="country")
    circuit: Mapped[list["Circuit"]] = relationship("Circuit", back_populates="country")
    constructor: Mapped[list["Constructor"]] = relationship("Constructor", back_populates="country")
    driver: Mapped[list["Driver"]] = relationship(
        "Driver", foreign_keys="[Driver.country_of_birth_country_id]", back_populates="country_of_birth_country"
    )
    driver_: Mapped[list["Driver"]] = relationship(
        "Driver", foreign_keys="[Driver.nationality_country_id]", back_populates="nationality_country"
    )
    driver1: Mapped[list["Driver"]] = relationship(
        "Driver", foreign_keys="[Driver.second_nationality_country_id]", back_populates="second_nationality_country"
    )
    engine_manufacturer: Mapped[list["EngineManufacturer"]] = relationship(
        "EngineManufacturer", back_populates="country"
    )
    grand_prix: Mapped[list["GrandPrix"]] = relationship("GrandPrix", back_populates="country")
    season_entrant: Mapped[list["SeasonEntrant"]] = relationship("SeasonEntrant", back_populates="country")
    tyre_manufacturer: Mapped[list["TyreManufacturer"]] = relationship("TyreManufacturer", back_populates="country")


class Circuit(Base):
    __tablename__ = "circuit"
    __table_args__ = (
        ForeignKeyConstraint(["country_id"], ["country.id"], name="circuit_country_id_fkey"),
        PrimaryKeyConstraint("id", name="circuit_pkey"),
        Index("crct_country_id_idx", "country_id"),
        Index("crct_direction_idx", "direction"),
        Index("crct_full_name_idx", "full_name"),
        Index("crct_name_idx", "name"),
        Index("crct_place_name_idx", "place_name"),
        Index("crct_type_idx", "type"),
    )

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(6), nullable=False)
    direction: Mapped[str] = mapped_column(String(14), nullable=False)
    place_name: Mapped[str] = mapped_column(String(100), nullable=False)
    country_id: Mapped[str] = mapped_column(String(100), nullable=False)
    latitude: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 6), nullable=False)
    longitude: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 6), nullable=False)
    length: Mapped[decimal.Decimal] = mapped_column(Numeric(6, 3), nullable=False)
    turns: Mapped[int] = mapped_column(Integer, nullable=False)
    total_races_held: Mapped[int] = mapped_column(Integer, nullable=False)
    previous_names: Mapped[Optional[str]] = mapped_column(String(255))

    country: Mapped["Country"] = relationship("Country", back_populates="circuit")
    race: Mapped[list["Race"]] = relationship("Race", back_populates="circuit")


class Constructor(Base):
    __tablename__ = "constructor"
    __table_args__ = (
        ForeignKeyConstraint(["country_id"], ["country.id"], name="constructor_country_id_fkey"),
        PrimaryKeyConstraint("id", name="constructor_pkey"),
        Index("cnst_country_id_idx", "country_id"),
        Index("cnst_full_name_idx", "full_name"),
        Index("cnst_name_idx", "name"),
    )

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    country_id: Mapped[str] = mapped_column(String(100), nullable=False)
    total_championship_wins: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_entries: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_starts: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_wins: Mapped[int] = mapped_column(Integer, nullable=False)
    total_1_and_2_finishes: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_laps: Mapped[int] = mapped_column(Integer, nullable=False)
    total_podiums: Mapped[int] = mapped_column(Integer, nullable=False)
    total_podium_races: Mapped[int] = mapped_column(Integer, nullable=False)
    total_points: Mapped[decimal.Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    total_championship_points: Mapped[decimal.Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    total_pole_positions: Mapped[int] = mapped_column(Integer, nullable=False)
    total_fastest_laps: Mapped[int] = mapped_column(Integer, nullable=False)
    best_championship_position: Mapped[Optional[int]] = mapped_column(Integer)
    best_starting_grid_position: Mapped[Optional[int]] = mapped_column(Integer)
    best_race_result: Mapped[Optional[int]] = mapped_column(Integer)

    country: Mapped["Country"] = relationship("Country", back_populates="constructor")
    chassis: Mapped[list["Chassis"]] = relationship("Chassis", back_populates="constructor")
    constructor_chronology: Mapped[list["ConstructorChronology"]] = relationship(
        "ConstructorChronology", foreign_keys="[ConstructorChronology.constructor_id]", back_populates="constructor"
    )
    constructor_chronology_: Mapped[list["ConstructorChronology"]] = relationship(
        "ConstructorChronology",
        foreign_keys="[ConstructorChronology.other_constructor_id]",
        back_populates="other_constructor",
    )
    season_constructor: Mapped[list["SeasonConstructor"]] = relationship(
        "SeasonConstructor", back_populates="constructor"
    )
    season_constructor_standing: Mapped[list["SeasonConstructorStanding"]] = relationship(
        "SeasonConstructorStanding", back_populates="constructor"
    )
    season_entrant_constructor: Mapped[list["SeasonEntrantConstructor"]] = relationship(
        "SeasonEntrantConstructor", back_populates="constructor"
    )
    season_entrant_driver: Mapped[list["SeasonEntrantDriver"]] = relationship(
        "SeasonEntrantDriver", back_populates="constructor"
    )
    season_entrant_tyre_manufacturer: Mapped[list["SeasonEntrantTyreManufacturer"]] = relationship(
        "SeasonEntrantTyreManufacturer", back_populates="constructor"
    )
    race_constructor_standing: Mapped[list["RaceConstructorStanding"]] = relationship(
        "RaceConstructorStanding", back_populates="constructor"
    )
    race_data: Mapped[list["RaceData"]] = relationship("RaceData", back_populates="constructor")
    season_entrant_chassis: Mapped[list["SeasonEntrantChassis"]] = relationship(
        "SeasonEntrantChassis", back_populates="constructor"
    )
    season_entrant_engine: Mapped[list["SeasonEntrantEngine"]] = relationship(
        "SeasonEntrantEngine", back_populates="constructor"
    )


class Driver(Base):
    __tablename__ = "driver"
    __table_args__ = (
        ForeignKeyConstraint(
            ["country_of_birth_country_id"], ["country.id"], name="driver_country_of_birth_country_id_fkey"
        ),
        ForeignKeyConstraint(["nationality_country_id"], ["country.id"], name="driver_nationality_country_id_fkey"),
        ForeignKeyConstraint(
            ["second_nationality_country_id"], ["country.id"], name="driver_second_nationality_country_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="driver_pkey"),
        Index("drvr_abbreviation_idx", "abbreviation"),
        Index("drvr_country_of_birth_country_id_idx", "country_of_birth_country_id"),
        Index("drvr_date_of_birth_idx", "date_of_birth"),
        Index("drvr_date_of_death_idx", "date_of_death"),
        Index("drvr_first_name_idx", "first_name"),
        Index("drvr_full_name_idx", "full_name"),
        Index("drvr_gender_idx", "gender"),
        Index("drvr_last_name_idx", "last_name"),
        Index("drvr_name_idx", "name"),
        Index("drvr_nationality_country_id_idx", "nationality_country_id"),
        Index("drvr_permanent_number_idx", "permanent_number"),
        Index("drvr_place_of_birth_idx", "place_of_birth"),
        Index("drvr_second_nationality_country_id_idx", "second_nationality_country_id"),
    )

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    abbreviation: Mapped[str] = mapped_column(String(3), nullable=False)
    gender: Mapped[str] = mapped_column(String(6), nullable=False)
    date_of_birth: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    place_of_birth: Mapped[str] = mapped_column(String(100), nullable=False)
    country_of_birth_country_id: Mapped[str] = mapped_column(String(100), nullable=False)
    nationality_country_id: Mapped[str] = mapped_column(String(100), nullable=False)
    total_championship_wins: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_entries: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_starts: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_wins: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_laps: Mapped[int] = mapped_column(Integer, nullable=False)
    total_podiums: Mapped[int] = mapped_column(Integer, nullable=False)
    total_points: Mapped[decimal.Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    total_championship_points: Mapped[decimal.Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    total_pole_positions: Mapped[int] = mapped_column(Integer, nullable=False)
    total_fastest_laps: Mapped[int] = mapped_column(Integer, nullable=False)
    total_driver_of_the_day: Mapped[int] = mapped_column(Integer, nullable=False)
    total_grand_slams: Mapped[int] = mapped_column(Integer, nullable=False)
    permanent_number: Mapped[Optional[str]] = mapped_column(String(2))
    date_of_death: Mapped[Optional[datetime.date]] = mapped_column(Date)
    second_nationality_country_id: Mapped[Optional[str]] = mapped_column(String(100))
    best_championship_position: Mapped[Optional[int]] = mapped_column(Integer)
    best_starting_grid_position: Mapped[Optional[int]] = mapped_column(Integer)
    best_race_result: Mapped[Optional[int]] = mapped_column(Integer)

    country_of_birth_country: Mapped["Country"] = relationship(
        "Country", foreign_keys=[country_of_birth_country_id], back_populates="driver"
    )
    nationality_country: Mapped["Country"] = relationship(
        "Country", foreign_keys=[nationality_country_id], back_populates="driver_"
    )
    second_nationality_country: Mapped[Optional["Country"]] = relationship(
        "Country", foreign_keys=[second_nationality_country_id], back_populates="driver1"
    )
    driver_family_relationship: Mapped[list["DriverFamilyRelationship"]] = relationship(
        "DriverFamilyRelationship", foreign_keys="[DriverFamilyRelationship.driver_id]", back_populates="driver"
    )
    driver_family_relationship_: Mapped[list["DriverFamilyRelationship"]] = relationship(
        "DriverFamilyRelationship",
        foreign_keys="[DriverFamilyRelationship.other_driver_id]",
        back_populates="other_driver",
    )
    season_driver: Mapped[list["SeasonDriver"]] = relationship("SeasonDriver", back_populates="driver")
    season_driver_standing: Mapped[list["SeasonDriverStanding"]] = relationship(
        "SeasonDriverStanding", back_populates="driver"
    )
    season_entrant_driver: Mapped[list["SeasonEntrantDriver"]] = relationship(
        "SeasonEntrantDriver", back_populates="driver"
    )
    race_data: Mapped[list["RaceData"]] = relationship("RaceData", back_populates="driver")
    race_driver_standing: Mapped[list["RaceDriverStanding"]] = relationship(
        "RaceDriverStanding", back_populates="driver"
    )


class EngineManufacturer(Base):
    __tablename__ = "engine_manufacturer"
    __table_args__ = (
        ForeignKeyConstraint(["country_id"], ["country.id"], name="engine_manufacturer_country_id_fkey"),
        PrimaryKeyConstraint("id", name="engine_manufacturer_pkey"),
        Index("enmf_country_id_idx", "country_id"),
        Index("enmf_name_idx", "name"),
    )

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country_id: Mapped[str] = mapped_column(String(100), nullable=False)
    total_championship_wins: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_entries: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_starts: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_wins: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_laps: Mapped[int] = mapped_column(Integer, nullable=False)
    total_podiums: Mapped[int] = mapped_column(Integer, nullable=False)
    total_podium_races: Mapped[int] = mapped_column(Integer, nullable=False)
    total_points: Mapped[decimal.Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    total_championship_points: Mapped[decimal.Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    total_pole_positions: Mapped[int] = mapped_column(Integer, nullable=False)
    total_fastest_laps: Mapped[int] = mapped_column(Integer, nullable=False)
    best_championship_position: Mapped[Optional[int]] = mapped_column(Integer)
    best_starting_grid_position: Mapped[Optional[int]] = mapped_column(Integer)
    best_race_result: Mapped[Optional[int]] = mapped_column(Integer)

    country: Mapped["Country"] = relationship("Country", back_populates="engine_manufacturer")
    engine: Mapped[list["Engine"]] = relationship("Engine", back_populates="engine_manufacturer")
    season_constructor_standing: Mapped[list["SeasonConstructorStanding"]] = relationship(
        "SeasonConstructorStanding", back_populates="engine_manufacturer"
    )
    season_engine_manufacturer: Mapped[list["SeasonEngineManufacturer"]] = relationship(
        "SeasonEngineManufacturer", back_populates="engine_manufacturer"
    )
    season_entrant_constructor: Mapped[list["SeasonEntrantConstructor"]] = relationship(
        "SeasonEntrantConstructor", back_populates="engine_manufacturer"
    )
    season_entrant_driver: Mapped[list["SeasonEntrantDriver"]] = relationship(
        "SeasonEntrantDriver", back_populates="engine_manufacturer"
    )
    season_entrant_tyre_manufacturer: Mapped[list["SeasonEntrantTyreManufacturer"]] = relationship(
        "SeasonEntrantTyreManufacturer", back_populates="engine_manufacturer"
    )
    race_constructor_standing: Mapped[list["RaceConstructorStanding"]] = relationship(
        "RaceConstructorStanding", back_populates="engine_manufacturer"
    )
    race_data: Mapped[list["RaceData"]] = relationship("RaceData", back_populates="engine_manufacturer")
    season_entrant_chassis: Mapped[list["SeasonEntrantChassis"]] = relationship(
        "SeasonEntrantChassis", back_populates="engine_manufacturer"
    )
    season_entrant_engine: Mapped[list["SeasonEntrantEngine"]] = relationship(
        "SeasonEntrantEngine", back_populates="engine_manufacturer"
    )


class GrandPrix(Base):
    __tablename__ = "grand_prix"
    __table_args__ = (
        ForeignKeyConstraint(["country_id"], ["country.id"], name="grand_prix_country_id_fkey"),
        PrimaryKeyConstraint("id", name="grand_prix_pkey"),
        Index("grpx_abbreviation_idx", "abbreviation"),
        Index("grpx_country_id_idx", "country_id"),
        Index("grpx_full_name_idx", "full_name"),
        Index("grpx_name_idx", "name"),
        Index("grpx_short_name_idx", "short_name"),
    )

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    short_name: Mapped[str] = mapped_column(String(100), nullable=False)
    abbreviation: Mapped[str] = mapped_column(String(3), nullable=False)
    total_races_held: Mapped[int] = mapped_column(Integer, nullable=False)
    country_id: Mapped[Optional[str]] = mapped_column(String(100))

    country: Mapped[Optional["Country"]] = relationship("Country", back_populates="grand_prix")
    race: Mapped[list["Race"]] = relationship("Race", back_populates="grand_prix")


class SeasonEntrant(Base):
    __tablename__ = "season_entrant"
    __table_args__ = (
        ForeignKeyConstraint(["country_id"], ["country.id"], name="season_entrant_country_id_fkey"),
        ForeignKeyConstraint(["entrant_id"], ["entrant.id"], name="season_entrant_entrant_id_fkey"),
        ForeignKeyConstraint(["year"], ["season.year"], name="season_entrant_year_fkey"),
        PrimaryKeyConstraint("year", "entrant_id", name="season_entrant_pkey"),
        Index("sent_country_id_idx", "country_id"),
        Index("sent_entrant_id_idx", "entrant_id"),
        Index("sent_year_idx", "year"),
    )

    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    entrant_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    country_id: Mapped[str] = mapped_column(String(100), nullable=False)

    country: Mapped["Country"] = relationship("Country", back_populates="season_entrant")
    entrant: Mapped["Entrant"] = relationship("Entrant", back_populates="season_entrant")
    season: Mapped["Season"] = relationship("Season", back_populates="season_entrant")


class TyreManufacturer(Base):
    __tablename__ = "tyre_manufacturer"
    __table_args__ = (
        ForeignKeyConstraint(["country_id"], ["country.id"], name="tyre_manufacturer_country_id_fkey"),
        PrimaryKeyConstraint("id", name="tyre_manufacturer_pkey"),
        Index("tymf_country_id_idx", "country_id"),
        Index("tymf_name_idx", "name"),
    )

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country_id: Mapped[str] = mapped_column(String(100), nullable=False)
    total_race_entries: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_starts: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_wins: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_laps: Mapped[int] = mapped_column(Integer, nullable=False)
    total_podiums: Mapped[int] = mapped_column(Integer, nullable=False)
    total_podium_races: Mapped[int] = mapped_column(Integer, nullable=False)
    total_pole_positions: Mapped[int] = mapped_column(Integer, nullable=False)
    total_fastest_laps: Mapped[int] = mapped_column(Integer, nullable=False)
    best_starting_grid_position: Mapped[Optional[int]] = mapped_column(Integer)
    best_race_result: Mapped[Optional[int]] = mapped_column(Integer)

    country: Mapped["Country"] = relationship("Country", back_populates="tyre_manufacturer")
    season_entrant_tyre_manufacturer: Mapped[list["SeasonEntrantTyreManufacturer"]] = relationship(
        "SeasonEntrantTyreManufacturer", back_populates="tyre_manufacturer"
    )
    season_tyre_manufacturer: Mapped[list["SeasonTyreManufacturer"]] = relationship(
        "SeasonTyreManufacturer", back_populates="tyre_manufacturer"
    )
    race_data: Mapped[list["RaceData"]] = relationship("RaceData", back_populates="tyre_manufacturer")


class Chassis(Base):
    __tablename__ = "chassis"
    __table_args__ = (
        ForeignKeyConstraint(["constructor_id"], ["constructor.id"], name="chassis_constructor_id_fkey"),
        PrimaryKeyConstraint("id", name="chassis_pkey"),
        Index("chss_constructor_id_idx", "constructor_id"),
        Index("chss_full_name_idx", "full_name"),
        Index("chss_name_idx", "name"),
    )

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    constructor_id: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)

    constructor: Mapped["Constructor"] = relationship("Constructor", back_populates="chassis")
    season_entrant_chassis: Mapped[list["SeasonEntrantChassis"]] = relationship(
        "SeasonEntrantChassis", back_populates="chassis"
    )


class ConstructorChronology(Base):
    __tablename__ = "constructor_chronology"
    __table_args__ = (
        ForeignKeyConstraint(["constructor_id"], ["constructor.id"], name="constructor_chronology_constructor_id_fkey"),
        ForeignKeyConstraint(
            ["other_constructor_id"], ["constructor.id"], name="constructor_chronology_other_constructor_id_fkey"
        ),
        PrimaryKeyConstraint("constructor_id", "position_display_order", name="constructor_chronology_pkey"),
        UniqueConstraint(
            "constructor_id",
            "other_constructor_id",
            "year_from",
            "year_to",
            name="constructor_chronology_constructor_id_other_constructor_id__key",
        ),
        Index("cnch_constructor_id_idx", "constructor_id"),
        Index("cnch_other_constructor_id_idx", "other_constructor_id"),
        Index("cnch_position_display_order_idx", "position_display_order"),
    )

    constructor_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    position_display_order: Mapped[int] = mapped_column(Integer, primary_key=True)
    other_constructor_id: Mapped[str] = mapped_column(String(100), nullable=False)
    year_from: Mapped[int] = mapped_column(Integer, nullable=False)
    year_to: Mapped[Optional[int]] = mapped_column(Integer)

    constructor: Mapped["Constructor"] = relationship(
        "Constructor", foreign_keys=[constructor_id], back_populates="constructor_chronology"
    )
    other_constructor: Mapped["Constructor"] = relationship(
        "Constructor", foreign_keys=[other_constructor_id], back_populates="constructor_chronology_"
    )


class DriverFamilyRelationship(Base):
    __tablename__ = "driver_family_relationship"
    __table_args__ = (
        ForeignKeyConstraint(["driver_id"], ["driver.id"], name="driver_family_relationship_driver_id_fkey"),
        ForeignKeyConstraint(
            ["other_driver_id"], ["driver.id"], name="driver_family_relationship_other_driver_id_fkey"
        ),
        PrimaryKeyConstraint("driver_id", "position_display_order", name="driver_family_relationship_pkey"),
        UniqueConstraint(
            "driver_id", "other_driver_id", "type", name="driver_family_relationship_driver_id_other_driver_id_type_key"
        ),
        Index("dfrl_driver_id_idx", "driver_id"),
        Index("dfrl_other_driver_id_idx", "other_driver_id"),
        Index("dfrl_position_display_order_idx", "position_display_order"),
    )

    driver_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    position_display_order: Mapped[int] = mapped_column(Integer, primary_key=True)
    other_driver_id: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)

    driver: Mapped["Driver"] = relationship(
        "Driver", foreign_keys=[driver_id], back_populates="driver_family_relationship"
    )
    other_driver: Mapped["Driver"] = relationship(
        "Driver", foreign_keys=[other_driver_id], back_populates="driver_family_relationship_"
    )


class Engine(Base):
    __tablename__ = "engine"
    __table_args__ = (
        ForeignKeyConstraint(
            ["engine_manufacturer_id"], ["engine_manufacturer.id"], name="engine_engine_manufacturer_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="engine_pkey"),
        Index("engn_aspiration_idx", "aspiration"),
        Index("engn_capacity_idx", "capacity"),
        Index("engn_configuration_idx", "configuration"),
        Index("engn_engine_manufacturer_id_idx", "engine_manufacturer_id"),
        Index("engn_full_name_idx", "full_name"),
        Index("engn_name_idx", "name"),
    )

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    engine_manufacturer_id: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    capacity: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(2, 1))
    configuration: Mapped[Optional[str]] = mapped_column(String(100))
    aspiration: Mapped[Optional[str]] = mapped_column(String(100))

    engine_manufacturer: Mapped["EngineManufacturer"] = relationship("EngineManufacturer", back_populates="engine")
    season_entrant_engine: Mapped[list["SeasonEntrantEngine"]] = relationship(
        "SeasonEntrantEngine", back_populates="engine"
    )


class Race(Base):
    __tablename__ = "race"
    __table_args__ = (
        ForeignKeyConstraint(["circuit_id"], ["circuit.id"], name="race_circuit_id_fkey"),
        ForeignKeyConstraint(["grand_prix_id"], ["grand_prix.id"], name="race_grand_prix_id_fkey"),
        ForeignKeyConstraint(["year"], ["season.year"], name="race_year_fkey"),
        PrimaryKeyConstraint("id", name="race_pkey"),
        UniqueConstraint("year", "round", name="race_year_round_key"),
        Index("race_circuit_id_idx", "circuit_id"),
        Index("race_circuit_type_idx", "circuit_type"),
        Index("race_date_idx", "date"),
        Index("race_direction_idx", "direction"),
        Index("race_grand_prix_id_idx", "grand_prix_id"),
        Index("race_official_name_idx", "official_name"),
        Index("race_qualifying_format_idx", "qualifying_format"),
        Index("race_round_idx", "round"),
        Index("race_sprint_qualifying_format_idx", "sprint_qualifying_format"),
        Index("race_year_idx", "year"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    round: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    grand_prix_id: Mapped[str] = mapped_column(String(100), nullable=False)
    official_name: Mapped[str] = mapped_column(String(100), nullable=False)
    qualifying_format: Mapped[str] = mapped_column(String(20), nullable=False)
    circuit_id: Mapped[str] = mapped_column(String(100), nullable=False)
    circuit_type: Mapped[str] = mapped_column(String(6), nullable=False)
    direction: Mapped[str] = mapped_column(String(14), nullable=False)
    course_length: Mapped[decimal.Decimal] = mapped_column(Numeric(6, 3), nullable=False)
    turns: Mapped[int] = mapped_column(Integer, nullable=False)
    laps: Mapped[int] = mapped_column(Integer, nullable=False)
    distance: Mapped[decimal.Decimal] = mapped_column(Numeric(6, 3), nullable=False)
    time: Mapped[Optional[str]] = mapped_column(String(5))
    sprint_qualifying_format: Mapped[Optional[str]] = mapped_column(String(20))
    scheduled_laps: Mapped[Optional[int]] = mapped_column(Integer)
    scheduled_distance: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(6, 3))
    drivers_championship_decider: Mapped[Optional[bool]] = mapped_column(Boolean)
    constructors_championship_decider: Mapped[Optional[bool]] = mapped_column(Boolean)
    pre_qualifying_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    pre_qualifying_time: Mapped[Optional[str]] = mapped_column(String(5))
    free_practice_1_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    free_practice_1_time: Mapped[Optional[str]] = mapped_column(String(5))
    free_practice_2_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    free_practice_2_time: Mapped[Optional[str]] = mapped_column(String(5))
    free_practice_3_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    free_practice_3_time: Mapped[Optional[str]] = mapped_column(String(5))
    free_practice_4_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    free_practice_4_time: Mapped[Optional[str]] = mapped_column(String(5))
    qualifying_1_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    qualifying_1_time: Mapped[Optional[str]] = mapped_column(String(5))
    qualifying_2_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    qualifying_2_time: Mapped[Optional[str]] = mapped_column(String(5))
    qualifying_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    qualifying_time: Mapped[Optional[str]] = mapped_column(String(5))
    sprint_qualifying_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    sprint_qualifying_time: Mapped[Optional[str]] = mapped_column(String(5))
    sprint_race_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    sprint_race_time: Mapped[Optional[str]] = mapped_column(String(5))
    warming_up_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    warming_up_time: Mapped[Optional[str]] = mapped_column(String(5))

    circuit: Mapped["Circuit"] = relationship("Circuit", back_populates="race")
    grand_prix: Mapped["GrandPrix"] = relationship("GrandPrix", back_populates="race")
    season: Mapped["Season"] = relationship("Season", back_populates="race")
    race_constructor_standing: Mapped[list["RaceConstructorStanding"]] = relationship(
        "RaceConstructorStanding", back_populates="race"
    )
    race_data: Mapped[list["RaceData"]] = relationship("RaceData", back_populates="race")
    race_driver_standing: Mapped[list["RaceDriverStanding"]] = relationship("RaceDriverStanding", back_populates="race")


class SeasonConstructor(Base):
    __tablename__ = "season_constructor"
    __table_args__ = (
        ForeignKeyConstraint(["constructor_id"], ["constructor.id"], name="season_constructor_constructor_id_fkey"),
        ForeignKeyConstraint(["year"], ["season.year"], name="season_constructor_year_fkey"),
        PrimaryKeyConstraint("year", "constructor_id", name="season_constructor_pkey"),
        Index("sscn_constructor_id_idx", "constructor_id"),
        Index("sscn_year_idx", "year"),
    )

    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    constructor_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    total_race_entries: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_starts: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_wins: Mapped[int] = mapped_column(Integer, nullable=False)
    total_1_and_2_finishes: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_laps: Mapped[int] = mapped_column(Integer, nullable=False)
    total_podiums: Mapped[int] = mapped_column(Integer, nullable=False)
    total_podium_races: Mapped[int] = mapped_column(Integer, nullable=False)
    total_points: Mapped[decimal.Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    total_pole_positions: Mapped[int] = mapped_column(Integer, nullable=False)
    total_fastest_laps: Mapped[int] = mapped_column(Integer, nullable=False)
    position_number: Mapped[Optional[int]] = mapped_column(Integer)
    position_text: Mapped[Optional[str]] = mapped_column(String(4))
    best_starting_grid_position: Mapped[Optional[int]] = mapped_column(Integer)
    best_race_result: Mapped[Optional[int]] = mapped_column(Integer)

    constructor: Mapped["Constructor"] = relationship("Constructor", back_populates="season_constructor")
    season: Mapped["Season"] = relationship("Season", back_populates="season_constructor")


class SeasonConstructorStanding(Base):
    __tablename__ = "season_constructor_standing"
    __table_args__ = (
        ForeignKeyConstraint(
            ["constructor_id"], ["constructor.id"], name="season_constructor_standing_constructor_id_fkey"
        ),
        ForeignKeyConstraint(
            ["engine_manufacturer_id"],
            ["engine_manufacturer.id"],
            name="season_constructor_standing_engine_manufacturer_id_fkey",
        ),
        ForeignKeyConstraint(["year"], ["season.year"], name="season_constructor_standing_year_fkey"),
        PrimaryKeyConstraint("year", "position_display_order", name="season_constructor_standing_pkey"),
        Index("sscs_constructor_id_idx", "constructor_id"),
        Index("sscs_engine_manufacturer_id_idx", "engine_manufacturer_id"),
        Index("sscs_position_display_order_idx", "position_display_order"),
        Index("sscs_position_number_idx", "position_number"),
        Index("sscs_position_text_idx", "position_text"),
        Index("sscs_year_idx", "year"),
    )

    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_display_order: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_text: Mapped[str] = mapped_column(String(4), nullable=False)
    constructor_id: Mapped[str] = mapped_column(String(100), nullable=False)
    engine_manufacturer_id: Mapped[str] = mapped_column(String(100), nullable=False)
    points: Mapped[decimal.Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    position_number: Mapped[Optional[int]] = mapped_column(Integer)

    constructor: Mapped["Constructor"] = relationship("Constructor", back_populates="season_constructor_standing")
    engine_manufacturer: Mapped["EngineManufacturer"] = relationship(
        "EngineManufacturer", back_populates="season_constructor_standing"
    )
    season: Mapped["Season"] = relationship("Season", back_populates="season_constructor_standing")


class SeasonDriver(Base):
    __tablename__ = "season_driver"
    __table_args__ = (
        ForeignKeyConstraint(["driver_id"], ["driver.id"], name="season_driver_driver_id_fkey"),
        ForeignKeyConstraint(["year"], ["season.year"], name="season_driver_year_fkey"),
        PrimaryKeyConstraint("year", "driver_id", name="season_driver_pkey"),
        Index("ssdr_driver_id_idx", "driver_id"),
        Index("ssdr_year_idx", "year"),
    )

    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    driver_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    total_race_entries: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_starts: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_wins: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_laps: Mapped[int] = mapped_column(Integer, nullable=False)
    total_podiums: Mapped[int] = mapped_column(Integer, nullable=False)
    total_points: Mapped[decimal.Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    total_pole_positions: Mapped[int] = mapped_column(Integer, nullable=False)
    total_fastest_laps: Mapped[int] = mapped_column(Integer, nullable=False)
    total_driver_of_the_day: Mapped[int] = mapped_column(Integer, nullable=False)
    total_grand_slams: Mapped[int] = mapped_column(Integer, nullable=False)
    position_number: Mapped[Optional[int]] = mapped_column(Integer)
    position_text: Mapped[Optional[str]] = mapped_column(String(4))
    best_starting_grid_position: Mapped[Optional[int]] = mapped_column(Integer)
    best_race_result: Mapped[Optional[int]] = mapped_column(Integer)

    driver: Mapped["Driver"] = relationship("Driver", back_populates="season_driver")
    season: Mapped["Season"] = relationship("Season", back_populates="season_driver")


class SeasonDriverStanding(Base):
    __tablename__ = "season_driver_standing"
    __table_args__ = (
        ForeignKeyConstraint(["driver_id"], ["driver.id"], name="season_driver_standing_driver_id_fkey"),
        ForeignKeyConstraint(["year"], ["season.year"], name="season_driver_standing_year_fkey"),
        PrimaryKeyConstraint("year", "position_display_order", name="season_driver_standing_pkey"),
        Index("ssds_driver_id_idx", "driver_id"),
        Index("ssds_position_display_order_idx", "position_display_order"),
        Index("ssds_position_number_idx", "position_number"),
        Index("ssds_position_text_idx", "position_text"),
        Index("ssds_year_idx", "year"),
    )

    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_display_order: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_text: Mapped[str] = mapped_column(String(4), nullable=False)
    driver_id: Mapped[str] = mapped_column(String(100), nullable=False)
    points: Mapped[decimal.Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    position_number: Mapped[Optional[int]] = mapped_column(Integer)

    driver: Mapped["Driver"] = relationship("Driver", back_populates="season_driver_standing")
    season: Mapped["Season"] = relationship("Season", back_populates="season_driver_standing")


class SeasonEngineManufacturer(Base):
    __tablename__ = "season_engine_manufacturer"
    __table_args__ = (
        ForeignKeyConstraint(
            ["engine_manufacturer_id"],
            ["engine_manufacturer.id"],
            name="season_engine_manufacturer_engine_manufacturer_id_fkey",
        ),
        ForeignKeyConstraint(["year"], ["season.year"], name="season_engine_manufacturer_year_fkey"),
        PrimaryKeyConstraint("year", "engine_manufacturer_id", name="season_engine_manufacturer_pkey"),
        Index("ssem_engine_manufacturer_id_idx", "engine_manufacturer_id"),
        Index("ssem_year_idx", "year"),
    )

    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    engine_manufacturer_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    total_race_entries: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_starts: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_wins: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_laps: Mapped[int] = mapped_column(Integer, nullable=False)
    total_podiums: Mapped[int] = mapped_column(Integer, nullable=False)
    total_podium_races: Mapped[int] = mapped_column(Integer, nullable=False)
    total_points: Mapped[decimal.Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    total_pole_positions: Mapped[int] = mapped_column(Integer, nullable=False)
    total_fastest_laps: Mapped[int] = mapped_column(Integer, nullable=False)
    position_number: Mapped[Optional[int]] = mapped_column(Integer)
    position_text: Mapped[Optional[str]] = mapped_column(String(4))
    best_starting_grid_position: Mapped[Optional[int]] = mapped_column(Integer)
    best_race_result: Mapped[Optional[int]] = mapped_column(Integer)

    engine_manufacturer: Mapped["EngineManufacturer"] = relationship(
        "EngineManufacturer", back_populates="season_engine_manufacturer"
    )
    season: Mapped["Season"] = relationship("Season", back_populates="season_engine_manufacturer")


class SeasonEntrantConstructor(Base):
    __tablename__ = "season_entrant_constructor"
    __table_args__ = (
        ForeignKeyConstraint(
            ["constructor_id"], ["constructor.id"], name="season_entrant_constructor_constructor_id_fkey"
        ),
        ForeignKeyConstraint(
            ["engine_manufacturer_id"],
            ["engine_manufacturer.id"],
            name="season_entrant_constructor_engine_manufacturer_id_fkey",
        ),
        ForeignKeyConstraint(["entrant_id"], ["entrant.id"], name="season_entrant_constructor_entrant_id_fkey"),
        ForeignKeyConstraint(["year"], ["season.year"], name="season_entrant_constructor_year_fkey"),
        PrimaryKeyConstraint(
            "year", "entrant_id", "constructor_id", "engine_manufacturer_id", name="season_entrant_constructor_pkey"
        ),
        Index("secn_constructor_id_idx", "constructor_id"),
        Index("secn_engine_manufacturer_id_idx", "engine_manufacturer_id"),
        Index("secn_entrant_id_idx", "entrant_id"),
        Index("secn_year_idx", "year"),
    )

    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    entrant_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    constructor_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    engine_manufacturer_id: Mapped[str] = mapped_column(String(100), primary_key=True)

    constructor: Mapped["Constructor"] = relationship("Constructor", back_populates="season_entrant_constructor")
    engine_manufacturer: Mapped["EngineManufacturer"] = relationship(
        "EngineManufacturer", back_populates="season_entrant_constructor"
    )
    entrant: Mapped["Entrant"] = relationship("Entrant", back_populates="season_entrant_constructor")
    season: Mapped["Season"] = relationship("Season", back_populates="season_entrant_constructor")


class SeasonEntrantDriver(Base):
    __tablename__ = "season_entrant_driver"
    __table_args__ = (
        ForeignKeyConstraint(["constructor_id"], ["constructor.id"], name="season_entrant_driver_constructor_id_fkey"),
        ForeignKeyConstraint(["driver_id"], ["driver.id"], name="season_entrant_driver_driver_id_fkey"),
        ForeignKeyConstraint(
            ["engine_manufacturer_id"],
            ["engine_manufacturer.id"],
            name="season_entrant_driver_engine_manufacturer_id_fkey",
        ),
        ForeignKeyConstraint(["entrant_id"], ["entrant.id"], name="season_entrant_driver_entrant_id_fkey"),
        ForeignKeyConstraint(["year"], ["season.year"], name="season_entrant_driver_year_fkey"),
        PrimaryKeyConstraint(
            "year",
            "entrant_id",
            "constructor_id",
            "engine_manufacturer_id",
            "driver_id",
            name="season_entrant_driver_pkey",
        ),
        Index("sedr_constructor_id_idx", "constructor_id"),
        Index("sedr_driver_id_idx", "driver_id"),
        Index("sedr_engine_manufacturer_id_idx", "engine_manufacturer_id"),
        Index("sedr_entrant_id_idx", "entrant_id"),
        Index("sedr_year_idx", "year"),
    )

    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    entrant_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    constructor_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    engine_manufacturer_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    driver_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    test_driver: Mapped[bool] = mapped_column(Boolean, nullable=False)
    rounds: Mapped[Optional[str]] = mapped_column(String(100))
    rounds_text: Mapped[Optional[str]] = mapped_column(String(100))

    constructor: Mapped["Constructor"] = relationship("Constructor", back_populates="season_entrant_driver")
    driver: Mapped["Driver"] = relationship("Driver", back_populates="season_entrant_driver")
    engine_manufacturer: Mapped["EngineManufacturer"] = relationship(
        "EngineManufacturer", back_populates="season_entrant_driver"
    )
    entrant: Mapped["Entrant"] = relationship("Entrant", back_populates="season_entrant_driver")
    season: Mapped["Season"] = relationship("Season", back_populates="season_entrant_driver")


class SeasonEntrantTyreManufacturer(Base):
    __tablename__ = "season_entrant_tyre_manufacturer"
    __table_args__ = (
        ForeignKeyConstraint(
            ["constructor_id"], ["constructor.id"], name="season_entrant_tyre_manufacturer_constructor_id_fkey"
        ),
        ForeignKeyConstraint(
            ["engine_manufacturer_id"],
            ["engine_manufacturer.id"],
            name="season_entrant_tyre_manufacturer_engine_manufacturer_id_fkey",
        ),
        ForeignKeyConstraint(["entrant_id"], ["entrant.id"], name="season_entrant_tyre_manufacturer_entrant_id_fkey"),
        ForeignKeyConstraint(
            ["tyre_manufacturer_id"],
            ["tyre_manufacturer.id"],
            name="season_entrant_tyre_manufacturer_tyre_manufacturer_id_fkey",
        ),
        ForeignKeyConstraint(["year"], ["season.year"], name="season_entrant_tyre_manufacturer_year_fkey"),
        PrimaryKeyConstraint(
            "year",
            "entrant_id",
            "constructor_id",
            "engine_manufacturer_id",
            "tyre_manufacturer_id",
            name="season_entrant_tyre_manufacturer_pkey",
        ),
        Index("setm_constructor_id_idx", "constructor_id"),
        Index("setm_engine_manufacturer_id_idx", "engine_manufacturer_id"),
        Index("setm_entrant_id_idx", "entrant_id"),
        Index("setm_tyre_manufacturer_id_idx", "tyre_manufacturer_id"),
        Index("setm_year_idx", "year"),
    )

    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    entrant_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    constructor_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    engine_manufacturer_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    tyre_manufacturer_id: Mapped[str] = mapped_column(String(100), primary_key=True)

    constructor: Mapped["Constructor"] = relationship("Constructor", back_populates="season_entrant_tyre_manufacturer")
    engine_manufacturer: Mapped["EngineManufacturer"] = relationship(
        "EngineManufacturer", back_populates="season_entrant_tyre_manufacturer"
    )
    entrant: Mapped["Entrant"] = relationship("Entrant", back_populates="season_entrant_tyre_manufacturer")
    tyre_manufacturer: Mapped["TyreManufacturer"] = relationship(
        "TyreManufacturer", back_populates="season_entrant_tyre_manufacturer"
    )
    season: Mapped["Season"] = relationship("Season", back_populates="season_entrant_tyre_manufacturer")


class SeasonTyreManufacturer(Base):
    __tablename__ = "season_tyre_manufacturer"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tyre_manufacturer_id"],
            ["tyre_manufacturer.id"],
            name="season_tyre_manufacturer_tyre_manufacturer_id_fkey",
        ),
        ForeignKeyConstraint(["year"], ["season.year"], name="season_tyre_manufacturer_year_fkey"),
        PrimaryKeyConstraint("year", "tyre_manufacturer_id", name="season_tyre_manufacturer_pkey"),
        Index("sstm_tyre_manufacturer_id_idx", "tyre_manufacturer_id"),
        Index("sstm_year_idx", "year"),
    )

    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    tyre_manufacturer_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    total_race_entries: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_starts: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_wins: Mapped[int] = mapped_column(Integer, nullable=False)
    total_race_laps: Mapped[int] = mapped_column(Integer, nullable=False)
    total_podiums: Mapped[int] = mapped_column(Integer, nullable=False)
    total_podium_races: Mapped[int] = mapped_column(Integer, nullable=False)
    total_pole_positions: Mapped[int] = mapped_column(Integer, nullable=False)
    total_fastest_laps: Mapped[int] = mapped_column(Integer, nullable=False)
    best_starting_grid_position: Mapped[Optional[int]] = mapped_column(Integer)
    best_race_result: Mapped[Optional[int]] = mapped_column(Integer)

    tyre_manufacturer: Mapped["TyreManufacturer"] = relationship(
        "TyreManufacturer", back_populates="season_tyre_manufacturer"
    )
    season: Mapped["Season"] = relationship("Season", back_populates="season_tyre_manufacturer")


class RaceConstructorStanding(Base):
    __tablename__ = "race_constructor_standing"
    __table_args__ = (
        ForeignKeyConstraint(
            ["constructor_id"], ["constructor.id"], name="race_constructor_standing_constructor_id_fkey"
        ),
        ForeignKeyConstraint(
            ["engine_manufacturer_id"],
            ["engine_manufacturer.id"],
            name="race_constructor_standing_engine_manufacturer_id_fkey",
        ),
        ForeignKeyConstraint(["race_id"], ["race.id"], name="race_constructor_standing_race_id_fkey"),
        PrimaryKeyConstraint("race_id", "position_display_order", name="race_constructor_standing_pkey"),
        Index("rccs_constructor_id_idx", "constructor_id"),
        Index("rccs_engine_manufacturer_id_idx", "engine_manufacturer_id"),
        Index("rccs_position_display_order_idx", "position_display_order"),
        Index("rccs_position_number_idx", "position_number"),
        Index("rccs_position_text_idx", "position_text"),
        Index("rccs_race_id_idx", "race_id"),
    )

    race_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_display_order: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_text: Mapped[str] = mapped_column(String(4), nullable=False)
    constructor_id: Mapped[str] = mapped_column(String(100), nullable=False)
    engine_manufacturer_id: Mapped[str] = mapped_column(String(100), nullable=False)
    points: Mapped[decimal.Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    position_number: Mapped[Optional[int]] = mapped_column(Integer)
    positions_gained: Mapped[Optional[int]] = mapped_column(Integer)

    constructor: Mapped["Constructor"] = relationship("Constructor", back_populates="race_constructor_standing")
    engine_manufacturer: Mapped["EngineManufacturer"] = relationship(
        "EngineManufacturer", back_populates="race_constructor_standing"
    )
    race: Mapped["Race"] = relationship("Race", back_populates="race_constructor_standing")


class RaceData(Base):
    __tablename__ = "race_data"
    __table_args__ = (
        ForeignKeyConstraint(["constructor_id"], ["constructor.id"], name="race_data_constructor_id_fkey"),
        ForeignKeyConstraint(["driver_id"], ["driver.id"], name="race_data_driver_id_fkey"),
        ForeignKeyConstraint(
            ["engine_manufacturer_id"], ["engine_manufacturer.id"], name="race_data_engine_manufacturer_id_fkey"
        ),
        ForeignKeyConstraint(["race_id"], ["race.id"], name="race_data_race_id_fkey"),
        ForeignKeyConstraint(
            ["tyre_manufacturer_id"], ["tyre_manufacturer.id"], name="race_data_tyre_manufacturer_id_fkey"
        ),
        PrimaryKeyConstraint("race_id", "type", "position_display_order", name="race_data_pkey"),
        Index("rcda_constructor_id_idx", "constructor_id"),
        Index("rcda_driver_id_idx", "driver_id"),
        Index("rcda_driver_number_idx", "driver_number"),
        Index("rcda_engine_manufacturer_id_idx", "engine_manufacturer_id"),
        Index("rcda_position_display_order_idx", "position_display_order"),
        Index("rcda_position_number_idx", "position_number"),
        Index("rcda_position_text_idx", "position_text"),
        Index("rcda_race_id_idx", "race_id"),
        Index("rcda_type_idx", "type"),
        Index("rcda_tyre_manufacturer_id_idx", "tyre_manufacturer_id"),
    )

    race_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(50), primary_key=True)
    position_display_order: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_text: Mapped[str] = mapped_column(String(4), nullable=False)
    driver_number: Mapped[str] = mapped_column(String(3), nullable=False)
    driver_id: Mapped[str] = mapped_column(String(100), nullable=False)
    constructor_id: Mapped[str] = mapped_column(String(100), nullable=False)
    engine_manufacturer_id: Mapped[str] = mapped_column(String(100), nullable=False)
    tyre_manufacturer_id: Mapped[str] = mapped_column(String(100), nullable=False)
    position_number: Mapped[Optional[int]] = mapped_column(Integer)
    practice_time: Mapped[Optional[str]] = mapped_column(String(20))
    practice_time_millis: Mapped[Optional[int]] = mapped_column(Integer)
    practice_gap: Mapped[Optional[str]] = mapped_column(String(20))
    practice_gap_millis: Mapped[Optional[int]] = mapped_column(Integer)
    practice_interval: Mapped[Optional[str]] = mapped_column(String(20))
    practice_interval_millis: Mapped[Optional[int]] = mapped_column(Integer)
    practice_laps: Mapped[Optional[int]] = mapped_column(Integer)
    qualifying_time: Mapped[Optional[str]] = mapped_column(String(20))
    qualifying_time_millis: Mapped[Optional[int]] = mapped_column(Integer)
    qualifying_q1: Mapped[Optional[str]] = mapped_column(String(20))
    qualifying_q1_millis: Mapped[Optional[int]] = mapped_column(Integer)
    qualifying_q2: Mapped[Optional[str]] = mapped_column(String(20))
    qualifying_q2_millis: Mapped[Optional[int]] = mapped_column(Integer)
    qualifying_q3: Mapped[Optional[str]] = mapped_column(String(20))
    qualifying_q3_millis: Mapped[Optional[int]] = mapped_column(Integer)
    qualifying_gap: Mapped[Optional[str]] = mapped_column(String(20))
    qualifying_gap_millis: Mapped[Optional[int]] = mapped_column(Integer)
    qualifying_interval: Mapped[Optional[str]] = mapped_column(String(20))
    qualifying_interval_millis: Mapped[Optional[int]] = mapped_column(Integer)
    qualifying_laps: Mapped[Optional[int]] = mapped_column(Integer)
    starting_grid_position_qualification_position_number: Mapped[Optional[int]] = mapped_column(Integer)
    starting_grid_position_qualification_position_text: Mapped[Optional[str]] = mapped_column(String(4))
    starting_grid_position_grid_penalty: Mapped[Optional[str]] = mapped_column(String(20))
    starting_grid_position_grid_penalty_positions: Mapped[Optional[int]] = mapped_column(Integer)
    starting_grid_position_time: Mapped[Optional[str]] = mapped_column(String(20))
    starting_grid_position_time_millis: Mapped[Optional[int]] = mapped_column(Integer)
    race_shared_car: Mapped[Optional[bool]] = mapped_column(Boolean)
    race_laps: Mapped[Optional[int]] = mapped_column(Integer)
    race_time: Mapped[Optional[str]] = mapped_column(String(20))
    race_time_millis: Mapped[Optional[int]] = mapped_column(Integer)
    race_time_penalty: Mapped[Optional[str]] = mapped_column(String(20))
    race_time_penalty_millis: Mapped[Optional[int]] = mapped_column(Integer)
    race_gap: Mapped[Optional[str]] = mapped_column(String(20))
    race_gap_millis: Mapped[Optional[int]] = mapped_column(Integer)
    race_gap_laps: Mapped[Optional[int]] = mapped_column(Integer)
    race_interval: Mapped[Optional[str]] = mapped_column(String(20))
    race_interval_millis: Mapped[Optional[int]] = mapped_column(Integer)
    race_reason_retired: Mapped[Optional[str]] = mapped_column(String(100))
    race_points: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(8, 2))
    race_pole_position: Mapped[Optional[bool]] = mapped_column(Boolean)
    race_qualification_position_number: Mapped[Optional[int]] = mapped_column(Integer)
    race_qualification_position_text: Mapped[Optional[str]] = mapped_column(String(4))
    race_grid_position_number: Mapped[Optional[int]] = mapped_column(Integer)
    race_grid_position_text: Mapped[Optional[str]] = mapped_column(String(2))
    race_positions_gained: Mapped[Optional[int]] = mapped_column(Integer)
    race_pit_stops: Mapped[Optional[int]] = mapped_column(Integer)
    race_fastest_lap: Mapped[Optional[bool]] = mapped_column(Boolean)
    race_driver_of_the_day: Mapped[Optional[bool]] = mapped_column(Boolean)
    race_grand_slam: Mapped[Optional[bool]] = mapped_column(Boolean)
    fastest_lap_lap: Mapped[Optional[int]] = mapped_column(Integer)
    fastest_lap_time: Mapped[Optional[str]] = mapped_column(String(20))
    fastest_lap_time_millis: Mapped[Optional[int]] = mapped_column(Integer)
    fastest_lap_gap: Mapped[Optional[str]] = mapped_column(String(20))
    fastest_lap_gap_millis: Mapped[Optional[int]] = mapped_column(Integer)
    fastest_lap_interval: Mapped[Optional[str]] = mapped_column(String(20))
    fastest_lap_interval_millis: Mapped[Optional[int]] = mapped_column(Integer)
    pit_stop_stop: Mapped[Optional[int]] = mapped_column(Integer)
    pit_stop_lap: Mapped[Optional[int]] = mapped_column(Integer)
    pit_stop_time: Mapped[Optional[str]] = mapped_column(String(20))
    pit_stop_time_millis: Mapped[Optional[int]] = mapped_column(Integer)
    driver_of_the_day_percentage: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(4, 1))

    constructor: Mapped["Constructor"] = relationship("Constructor", back_populates="race_data")
    driver: Mapped["Driver"] = relationship("Driver", back_populates="race_data")
    engine_manufacturer: Mapped["EngineManufacturer"] = relationship("EngineManufacturer", back_populates="race_data")
    race: Mapped["Race"] = relationship("Race", back_populates="race_data")
    tyre_manufacturer: Mapped["TyreManufacturer"] = relationship("TyreManufacturer", back_populates="race_data")


class RaceDriverStanding(Base):
    __tablename__ = "race_driver_standing"
    __table_args__ = (
        ForeignKeyConstraint(["driver_id"], ["driver.id"], name="race_driver_standing_driver_id_fkey"),
        ForeignKeyConstraint(["race_id"], ["race.id"], name="race_driver_standing_race_id_fkey"),
        PrimaryKeyConstraint("race_id", "position_display_order", name="race_driver_standing_pkey"),
        Index("rcds_driver_id_idx", "driver_id"),
        Index("rcds_position_display_order_idx", "position_display_order"),
        Index("rcds_position_number_idx", "position_number"),
        Index("rcds_position_text_idx", "position_text"),
        Index("rcds_race_id_idx", "race_id"),
    )

    race_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_display_order: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_text: Mapped[str] = mapped_column(String(4), nullable=False)
    driver_id: Mapped[str] = mapped_column(String(100), nullable=False)
    points: Mapped[decimal.Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    position_number: Mapped[Optional[int]] = mapped_column(Integer)
    positions_gained: Mapped[Optional[int]] = mapped_column(Integer)

    driver: Mapped["Driver"] = relationship("Driver", back_populates="race_driver_standing")
    race: Mapped["Race"] = relationship("Race", back_populates="race_driver_standing")


class SeasonEntrantChassis(Base):
    __tablename__ = "season_entrant_chassis"
    __table_args__ = (
        ForeignKeyConstraint(["chassis_id"], ["chassis.id"], name="season_entrant_chassis_chassis_id_fkey"),
        ForeignKeyConstraint(["constructor_id"], ["constructor.id"], name="season_entrant_chassis_constructor_id_fkey"),
        ForeignKeyConstraint(
            ["engine_manufacturer_id"],
            ["engine_manufacturer.id"],
            name="season_entrant_chassis_engine_manufacturer_id_fkey",
        ),
        ForeignKeyConstraint(["entrant_id"], ["entrant.id"], name="season_entrant_chassis_entrant_id_fkey"),
        ForeignKeyConstraint(["year"], ["season.year"], name="season_entrant_chassis_year_fkey"),
        PrimaryKeyConstraint(
            "year",
            "entrant_id",
            "constructor_id",
            "engine_manufacturer_id",
            "chassis_id",
            name="season_entrant_chassis_pkey",
        ),
        Index("sech_chassis_id_idx", "chassis_id"),
        Index("sech_constructor_id_idx", "constructor_id"),
        Index("sech_engine_manufacturer_id_idx", "engine_manufacturer_id"),
        Index("sech_entrant_id_idx", "entrant_id"),
        Index("sech_year_idx", "year"),
    )

    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    entrant_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    constructor_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    engine_manufacturer_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    chassis_id: Mapped[str] = mapped_column(String(100), primary_key=True)

    chassis: Mapped["Chassis"] = relationship("Chassis", back_populates="season_entrant_chassis")
    constructor: Mapped["Constructor"] = relationship("Constructor", back_populates="season_entrant_chassis")
    engine_manufacturer: Mapped["EngineManufacturer"] = relationship(
        "EngineManufacturer", back_populates="season_entrant_chassis"
    )
    entrant: Mapped["Entrant"] = relationship("Entrant", back_populates="season_entrant_chassis")
    season: Mapped["Season"] = relationship("Season", back_populates="season_entrant_chassis")


class SeasonEntrantEngine(Base):
    __tablename__ = "season_entrant_engine"
    __table_args__ = (
        ForeignKeyConstraint(["constructor_id"], ["constructor.id"], name="season_entrant_engine_constructor_id_fkey"),
        ForeignKeyConstraint(["engine_id"], ["engine.id"], name="season_entrant_engine_engine_id_fkey"),
        ForeignKeyConstraint(
            ["engine_manufacturer_id"],
            ["engine_manufacturer.id"],
            name="season_entrant_engine_engine_manufacturer_id_fkey",
        ),
        ForeignKeyConstraint(["entrant_id"], ["entrant.id"], name="season_entrant_engine_entrant_id_fkey"),
        ForeignKeyConstraint(["year"], ["season.year"], name="season_entrant_engine_year_fkey"),
        PrimaryKeyConstraint(
            "year",
            "entrant_id",
            "constructor_id",
            "engine_manufacturer_id",
            "engine_id",
            name="season_entrant_engine_pkey",
        ),
        Index("seen_constructor_id_idx", "constructor_id"),
        Index("seen_engine_id_idx", "engine_id"),
        Index("seen_engine_manufacturer_id_idx", "engine_manufacturer_id"),
        Index("seen_entrant_id_idx", "entrant_id"),
        Index("seen_year_idx", "year"),
    )

    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    entrant_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    constructor_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    engine_manufacturer_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    engine_id: Mapped[str] = mapped_column(String(100), primary_key=True)

    constructor: Mapped["Constructor"] = relationship("Constructor", back_populates="season_entrant_engine")
    engine: Mapped["Engine"] = relationship("Engine", back_populates="season_entrant_engine")
    engine_manufacturer: Mapped["EngineManufacturer"] = relationship(
        "EngineManufacturer", back_populates="season_entrant_engine"
    )
    entrant: Mapped["Entrant"] = relationship("Entrant", back_populates="season_entrant_engine")
    season: Mapped["Season"] = relationship("Season", back_populates="season_entrant_engine")
