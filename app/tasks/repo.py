from sqlalchemy import select
from sqlalchemy import func, and_, or_
from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.postgresql import insert


metadata = MetaData()


def insert_rundate(session, run_date):
    try:
        engine = session.get_bind()
        metadata.reflect(bind=engine)
        etl_runs = Table('etl_runs', metadata, autoload_with=engine)
        stmt = insert(etl_runs).values(run_date=run_date)
        stmt = stmt.on_conflict_do_nothing()
        session.execute(stmt)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def insert_listings(session, items):
    try:
        engine = session.get_bind()
        metadata.reflect(bind=engine)
        listings = Table('listings', metadata, autoload_with=engine)
        stmt = insert(listings).values(items)
        stmt = stmt.on_conflict_do_update(
            index_elements=[listings.c.bukken_id, listings.c.source],
            set_={"last_seen_at": stmt.excluded.last_seen_at},
        )
        session.execute(stmt)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def select_listings_missing_details(session, source):
    engine = session.get_bind()
    metadata.reflect(bind=engine)
    etl_runs = Table('etl_runs', metadata, autoload_with=engine)
    listings = Table('listings', metadata, autoload_with=engine)
    listings_details = Table('listings_details', metadata, autoload_with=engine)

    current = (
        select(
            listings.c.bukken_id,
            listings.c.source,
            listings.c.url,
        )
        .where(
            and_(
                listings.c.last_seen_at
                == select(func.max(etl_runs.c.run_date))
                .select_from(etl_runs)
                .scalar_subquery(),
                listings.c.source == source,
            )
        )
        .cte("current")
    )

    stmt = (
        select(current)
        .select_from(
            current.outerjoin(
                listings_details,
                and_(
                    current.c.bukken_id == listings_details.c.bukken_id,
                    current.c.source == listings_details.c.source,
                ),
            )
        )
        .where(
            or_(
                listings_details.c.bukken_id == None,
                listings_details.c.needs_update == True,
            )
        )
    )

    results = session.execute(stmt).fetchall()
    return [result._asdict() for result in results]


def select_coordinates(session, address):
    engine = session.get_bind()
    metadata.reflect(bind=engine)
    listings_details = Table('listings_details', metadata, autoload_with=engine)

    stmt = select(
        listings_details.c.lat,
        listings_details.c.lon,
    ).where(
        and_(
            listings_details.c.address == address,
            listings_details.c.is_geocoded,
        )
    )

    result = session.execute(stmt).fetchone()
    if result is None:
        coordinates = {"lat": None, "lon": None, "is_geocoded": True}
    else:
        coordinates = result._asdict()
        coordinates["is_geocoded"] = True
    return coordinates


def insert_listings_details(session, items):
    try:
        engine = session.get_bind()
        metadata.reflect(bind=engine)
        listings_details = Table('listings_details', metadata, autoload_with=engine)

        stmt = insert(listings_details).values(items)

        stmt = stmt.on_conflict_do_update(
            index_elements=[listings_details.c.bukken_id, listings_details.c.source],
            set_={
                "lat": stmt.excluded.lat,
                "lon": stmt.excluded.lon,
                "price_yen": stmt.excluded.price_yen,
                "address": stmt.excluded.address,
                "image_urls": stmt.excluded.image_urls,
                "construction_year": stmt.excluded.construction_year,
                "description": stmt.excluded.description,
                "remarks": stmt.excluded.remarks,
                "needs_update": False,
            },
        )
        session.execute(stmt)
        session.commit()

    except Exception as e:
        session.rollback()
        raise e

















# def select_listings_for_geojson():
#     with db.session.begin():
#         etl_runs = db.metadata.tables["etl_runs"]
#         listings = db.metadata.tables["listings"]
#         listings_details = db.metadata.tables["listings_details"]
#         listings_translations = db.metadata.tables["listings_translations"]
#         current = (
#             select(listings)
#             .where(
#                 listings.c.last_seen_at
#                 == select(func.max(etl_runs.c.run_date))
#                 .select_from(etl_runs)
#                 .scalar_subquery()
#             )
#             .cte("current")
#         )

#         stmt = (
#             select(
#                 listings_details.c.bukken_id,
#                 listings_details.c.source,
#                 current.c.url,
#                 listings_details.c.lat,
#                 listings_details.c.lon,
#                 listings_details.c.is_geocoded,
#                 listings_details.c.price_yen,
#                 listings_details.c.address,
#                 listings_translations.c.address.label("translated_address"),
#                 listings_details.c.image_urls,
#                 listings_details.c.construction_year,
#                 listings_details.c.description.label("description"),
#                 listings_translations.c.description.label("translated_description"),
#                 listings_details.c.remarks,
#                 listings_translations.c.remarks.label("translated_remarks"),
#                 current.c.first_seen_at,
#                 current.c.last_seen_at,
#             )
#             .select_from(current)
#             .join(
#                 listings_details,
#                 and_(
#                     current.c.bukken_id == listings_details.c.bukken_id,
#                     current.c.source == listings_details.c.source,
#                 ),
#             )
#             .join(
#                 listings_translations,
#                 and_(
#                     current.c.bukken_id == listings_translations.c.bukken_id,
#                     current.c.source == listings_translations.c.source,
#                 ),
#             )
#         )

#         results = db.session.execute(stmt).fetchall()
#         return [result._asdict() for result in results]


# def select_details_missing_translation():
#     with db.session.begin():
#         listings_details = db.metadata.tables["listings_details"]
#         listings_translations = db.metadata.tables["listings_translations"]
#         stmt = (
#             select(
#                 listings_details.c.bukken_id,
#                 listings_details.c.source,
#                 listings_details.c.description,
#                 listings_details.c.remarks,
#                 listings_details.c.address,
#             )
#             .select_from(
#                 listings_details.outerjoin(
#                     listings_translations,
#                     and_(
#                         listings_details.c.bukken_id == listings_translations.c.bukken_id,
#                         listings_details.c.source == listings_translations.c.source,
#                     ),
#                 )
#             )
#             .where(
#                 or_(
#                     listings_translations.c.bukken_id == None,
#                     listings_translations.c.needs_update == True,
#                 )
#             )
#         )
#         results = db.session.execute(stmt).fetchall()
#         return [result._asdict() for result in results]


# def insert_translations(items):
#     try:
#         with db.session.begin():
#             listings_translations = db.metadata.tables["listings_translations"]
#             stmt = listings_translations.insert().values(items)

#             stmt = stmt.on_conflict_do_update(
#                 index_elements=[
#                     listings_translations.c.bukken_id,
#                     listings_translations.c.source,
#                 ],
#                 set_={
#                     "address": stmt.excluded.address,
#                     "description": stmt.excluded.description,
#                     "remarks": stmt.excluded.remarks,
#                     "needs_update": False,
#                 },
#             )
#             db.session.execute(stmt)
#             db.session.commit()

#     except Exception as e:
#         db.session.rollback()
#         raise e
