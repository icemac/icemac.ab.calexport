"""Database initialisation and upgrading."""

import zope.generations.generations


GENERATION = 1


manager = zope.generations.generations.SchemaManager(
    minimum_generation=GENERATION,
    generation=GENERATION,
    package_name='icemac.ab.calexport.generations')
