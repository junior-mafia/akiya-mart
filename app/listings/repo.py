from sqlalchemy import select, and_, func
from app.extensions import db
from sqlalchemy import select


def fetch_listing_by_id(source, bukken_id):
    with db.session.begin():
        listings = db.metadata.tables["listings"]
        listings_details = db.metadata.tables["listings_details"]
        listings_translations = db.metadata.tables["listings_translations"]
        etl_runs = db.metadata.tables["etl_runs"]
        current = (
            select(listings)
            .where(
                listings.c.last_seen_at
                == select(func.max(etl_runs.c.run_date))
                .select_from(etl_runs)
                .scalar_subquery()
            )
            .cte("current")
        )

        stmt = (
            select(
                listings_details.c.bukken_id,
                listings_details.c.source,
                current.c.url,
                listings_details.c.lat,
                listings_details.c.lon,
                listings_details.c.is_geocoded,
                listings_details.c.price_yen,
                listings_details.c.address,
                listings_translations.c.address.label("translated_address"),
                listings_details.c.image_urls,
                listings_details.c.construction_year,
                listings_details.c.description.label("description"),
                listings_translations.c.description.label("translated_description"),
                listings_details.c.remarks,
                listings_translations.c.remarks.label("translated_remarks"),
                current.c.first_seen_at,
                current.c.last_seen_at,
            )
            .select_from(current)
            .join(
                listings_details,
                and_(
                    current.c.bukken_id == listings_details.c.bukken_id,
                    current.c.source == listings_details.c.source,
                ),
            )
            .join(
                listings_translations,
                and_(
                    current.c.bukken_id == listings_translations.c.bukken_id,
                    current.c.source == listings_translations.c.source,
                ),
            )
            .where(
                and_(
                    current.c.bukken_id == bukken_id,
                    current.c.source == source,
                )
            )
        )

        result = db.session.execute(stmt).fetchone()
        if result is None:
            return None
        else:
            return result._asdict()
