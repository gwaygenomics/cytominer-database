"""

"""

import os
import pytest
import sqlalchemy
import sqlalchemy.orm
import subprocess
import perturbation.base
import perturbation.database
import perturbation.models
import random
import subprocess
import time

docker_name = 'testdb_{:04d}'.format(random.randint(0, 9999))

@pytest.yield_fixture
def session():

    cmd = 'docker run --name {} -p 3210:5432 -P -e POSTGRES_PASSWORD=password -d postgres'.format(docker_name).split(' ')

    subprocess.check_output(cmd)

    time.sleep(7)

    cmd = 'PGPASSWORD=password psql -h localhost -p 3210 -U postgres -c "CREATE DATABASE testdb"'

    subprocess.check_output(cmd, shell=True)

    engine = sqlalchemy.create_engine('postgresql://postgres:password@localhost:3210/testdb')

    session = sqlalchemy.orm.sessionmaker(bind=engine)

    perturbation.base.Base.metadata.create_all(engine)

    yield session()

    engine.dispose()

    cmd = 'docker stop {}'.format(docker_name).split(' ')

    subprocess.check_output(cmd)

    cmd = 'docker rm {}'.format(docker_name).split(' ')

    subprocess.check_output(cmd)


def test_seed(session):
    subprocess.call(['./munge.sh', 'test/data'])

    perturbation.database.seed('test/data', 'postgresql://postgres:password@localhost:3210/testdb', 'views.sql')

    n_plates = 1
    n_channels = 3
    n_patterns = 3
    n_wells = 4
    n_images = 8
    n_objects = 40
    n_bins_raddist = 4
    n_scales_texture = 3
    n_moments_coefs = 30

    n_matches = n_objects * n_patterns
    n_edges = n_matches * n_channels
    n_intensities = n_matches * n_channels
    n_textures = n_matches * n_channels * n_scales_texture
    n_radial_distributions = n_matches * n_channels * n_bins_raddist
    n_locations = n_matches * n_channels
    n_shapes = n_matches
    n_coordinates = n_matches + n_shapes + (n_matches * n_channels * 2)
    n_moments = n_shapes * n_moments_coefs
    n_neighborhoods = n_matches
    n_correlations = n_matches * 5

    assert len(session.query(perturbation.models.Pattern).all()) == n_patterns
    assert len(session.query(perturbation.models.Plate).all()) == n_plates
    assert len(session.query(perturbation.models.Channel).all()) == n_channels
    assert len(session.query(perturbation.models.Well).all()) == n_wells
    assert len(session.query(perturbation.models.Image).all()) == n_images
    assert len(session.query(perturbation.models.Match).all()) == n_matches
    assert len(session.query(perturbation.models.Edge).all()) == n_edges
    assert len(session.query(perturbation.models.Intensity).all()) == n_intensities
    assert len(session.query(perturbation.models.Texture).all()) == n_textures
    assert len(session.query(perturbation.models.RadialDistribution).all()) == n_radial_distributions
    assert len(session.query(perturbation.models.Shape).all()) == n_shapes
    assert len(session.query(perturbation.models.Location).all()) == n_locations
    assert len(session.query(perturbation.models.Coordinate).all()) == n_coordinates
    assert len(session.query(perturbation.models.Moment).all()) == n_moments
    assert len(session.query(perturbation.models.Neighborhood).all()) == n_neighborhoods
    assert len(session.query(perturbation.models.Correlation).all()) == n_correlations

    correlations = session.query(perturbation.models.Correlation)

    assert correlations.filter(perturbation.models.Correlation.match is None).all() == []

    assert len(session.query(sqlalchemy.Table('view_correlations', perturbation.base.Base.metadata,
                                              autoload_with=session.connection())).all()) == n_correlations
    assert len(session.query(sqlalchemy.Table('view_edges', perturbation.base.Base.metadata,
                                              autoload_with=session.connection())).all()) == n_edges
    assert len(session.query(sqlalchemy.Table('view_intensities', perturbation.base.Base.metadata,
                                              autoload_with=session.connection())).all()) == n_intensities
    assert len(session.query(sqlalchemy.Table('view_locations', perturbation.base.Base.metadata,
                                              autoload_with=session.connection())).all()) == n_locations
    assert len(session.query(sqlalchemy.Table('view_moments', perturbation.base.Base.metadata,
                                              autoload_with=session.connection())).all()) == n_moments
    assert len(session.query(sqlalchemy.Table('view_neighborhoods', perturbation.base.Base.metadata,
                                              autoload_with=session.connection())).all()) == n_neighborhoods
    assert len(session.query(sqlalchemy.Table('view_radial_distributions', perturbation.base.Base.metadata,
                                              autoload_with=session.connection())).all()) == n_radial_distributions
    assert len(session.query(sqlalchemy.Table('view_shapes', perturbation.base.Base.metadata,
                                              autoload_with=session.connection())).all()) == n_shapes
    assert len(session.query(sqlalchemy.Table('view_textures', perturbation.base.Base.metadata,
                                              autoload_with=session.connection())).all()) == n_textures

    session.connection().close()