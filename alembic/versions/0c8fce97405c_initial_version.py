"""initial version

Revision ID: 0c8fce97405c
Revises: 
Create Date: 2016-04-22 10:42:54.641992

"""

# revision identifiers, used by Alembic.
revision = '0c8fce97405c'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('channels',
    sa.Column('id', perturbation.UUID.UUID(length=16), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_channels_description'), 'channels', ['description'], unique=False)
    op.create_table('coordinates',
    sa.Column('id', perturbation.UUID.UUID(length=16), nullable=False),
    sa.Column('abscissa', sa.Integer(), nullable=True),
    sa.Column('ordinate', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patterns',
    sa.Column('id', perturbation.UUID.UUID(length=16), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_patterns_description'), 'patterns', ['description'], unique=False)
    op.create_table('plates',
    sa.Column('id', perturbation.UUID.UUID(length=16), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plates_description'), 'plates', ['description'], unique=False)
    op.create_table('shapes',
    sa.Column('id', perturbation.UUID.UUID(length=16), nullable=False),
    sa.Column('center_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('area', sa.Float(), nullable=True),
    sa.Column('compactness', sa.Float(), nullable=True),
    sa.Column('eccentricity', sa.Float(), nullable=True),
    sa.Column('euler_number', sa.Float(), nullable=True),
    sa.Column('extent', sa.Float(), nullable=True),
    sa.Column('form_factor', sa.Float(), nullable=True),
    sa.Column('major_axis_length', sa.Float(), nullable=True),
    sa.Column('max_feret_diameter', sa.Float(), nullable=True),
    sa.Column('maximum_radius', sa.Float(), nullable=True),
    sa.Column('mean_radius', sa.Float(), nullable=True),
    sa.Column('median_radius', sa.Float(), nullable=True),
    sa.Column('min_feret_diameter', sa.Float(), nullable=True),
    sa.Column('minor_axis_length', sa.Float(), nullable=True),
    sa.Column('orientation', sa.Float(), nullable=True),
    sa.Column('perimeter', sa.Float(), nullable=True),
    sa.Column('solidity', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['center_id'], ['coordinates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_shapes_center_id'), 'shapes', ['center_id'], unique=False)
    op.create_table('wells',
    sa.Column('id', perturbation.UUID.UUID(length=16), nullable=False),
    sa.Column('plate_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['plate_id'], ['plates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wells_description'), 'wells', ['description'], unique=False)
    op.create_index(op.f('ix_wells_plate_id'), 'wells', ['plate_id'], unique=False)
    op.create_table('images',
    sa.Column('id', perturbation.UUID.UUID(length=16), nullable=False),
    sa.Column('well_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['well_id'], ['wells.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_images_description'), 'images', ['description'], unique=False)
    op.create_index(op.f('ix_images_well_id'), 'images', ['well_id'], unique=False)
    op.create_table('moments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shape_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('a', sa.Integer(), nullable=True),
    sa.Column('b', sa.Integer(), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['shape_id'], ['shapes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_moments_shape_id'), 'moments', ['shape_id'], unique=False)
    op.create_table('objects',
    sa.Column('id', perturbation.UUID.UUID(length=16), nullable=False),
    sa.Column('image_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('description', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_objects_description'), 'objects', ['description'], unique=False)
    op.create_index(op.f('ix_objects_image_id'), 'objects', ['image_id'], unique=False)
    op.create_table('quality',
    sa.Column('id', perturbation.UUID.UUID(length=16), nullable=False),
    sa.Column('image_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('count_cell_clump', sa.Integer(), nullable=True),
    sa.Column('count_debris', sa.Integer(), nullable=True),
    sa.Column('count_low_intensity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quality_image_id'), 'quality', ['image_id'], unique=False)
    op.create_table('neighborhoods',
    sa.Column('id', perturbation.UUID.UUID(length=16), nullable=False),
    sa.Column('closest_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('object_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('second_closest_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('angle_between_neighbors_5', sa.Float(), nullable=True),
    sa.Column('angle_between_neighbors_adjacent', sa.Float(), nullable=True),
    sa.Column('first_closest_distance_5', sa.Float(), nullable=True),
    sa.Column('first_closest_distance_adjacent', sa.Float(), nullable=True),
    sa.Column('first_closest_object_number_adjacent', sa.Integer(), nullable=True),
    sa.Column('number_of_neighbors_5', sa.Integer(), nullable=True),
    sa.Column('number_of_neighbors_adjacent', sa.Integer(), nullable=True),
    sa.Column('percent_touching_5', sa.Float(), nullable=True),
    sa.Column('percent_touching_adjacent', sa.Float(), nullable=True),
    sa.Column('second_closest_distance_5', sa.Float(), nullable=True),
    sa.Column('second_closest_distance_adjacent', sa.Float(), nullable=True),
    sa.Column('second_closest_object_number_adjacent', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['closest_id'], ['objects.id'], ),
    sa.ForeignKeyConstraint(['object_id'], ['objects.id'], ),
    sa.ForeignKeyConstraint(['second_closest_id'], ['objects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_neighborhoods_closest_id'), 'neighborhoods', ['closest_id'], unique=False)
    op.create_index(op.f('ix_neighborhoods_object_id'), 'neighborhoods', ['object_id'], unique=False)
    op.create_index(op.f('ix_neighborhoods_second_closest_id'), 'neighborhoods', ['second_closest_id'], unique=False)
    op.create_table('matches',
    sa.Column('id', perturbation.UUID.UUID(length=16), nullable=False),
    sa.Column('center_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('neighborhood_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('object_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('pattern_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('shape_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.ForeignKeyConstraint(['center_id'], ['coordinates.id'], ),
    sa.ForeignKeyConstraint(['neighborhood_id'], ['neighborhoods.id'], ),
    sa.ForeignKeyConstraint(['object_id'], ['objects.id'], ),
    sa.ForeignKeyConstraint(['pattern_id'], ['patterns.id'], ),
    sa.ForeignKeyConstraint(['shape_id'], ['shapes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_matches_center_id'), 'matches', ['center_id'], unique=False)
    op.create_index(op.f('ix_matches_neighborhood_id'), 'matches', ['neighborhood_id'], unique=False)
    op.create_index(op.f('ix_matches_object_id'), 'matches', ['object_id'], unique=False)
    op.create_index(op.f('ix_matches_pattern_id'), 'matches', ['pattern_id'], unique=False)
    op.create_index(op.f('ix_matches_shape_id'), 'matches', ['shape_id'], unique=False)
    op.create_table('correlations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dependent_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('independent_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('match_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('coefficient', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['dependent_id'], ['channels.id'], ),
    sa.ForeignKeyConstraint(['independent_id'], ['channels.id'], ),
    sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_correlations_dependent_id'), 'correlations', ['dependent_id'], unique=False)
    op.create_index(op.f('ix_correlations_independent_id'), 'correlations', ['independent_id'], unique=False)
    op.create_index(op.f('ix_correlations_match_id'), 'correlations', ['match_id'], unique=False)
    op.create_table('edges',
    sa.Column('id', perturbation.UUID.UUID(length=16), nullable=False),
    sa.Column('channel_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('match_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('integrated', sa.Float(), nullable=True),
    sa.Column('maximum', sa.Float(), nullable=True),
    sa.Column('mean', sa.Float(), nullable=True),
    sa.Column('minimum', sa.Float(), nullable=True),
    sa.Column('standard_deviation', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
    sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_edges_channel_id'), 'edges', ['channel_id'], unique=False)
    op.create_index(op.f('ix_edges_match_id'), 'edges', ['match_id'], unique=False)
    op.create_table('intensities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channel_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('match_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('first_quartile', sa.Float(), nullable=True),
    sa.Column('integrated', sa.Float(), nullable=True),
    sa.Column('mass_displacement', sa.Float(), nullable=True),
    sa.Column('maximum', sa.Float(), nullable=True),
    sa.Column('mean', sa.Float(), nullable=True),
    sa.Column('median', sa.Float(), nullable=True),
    sa.Column('median_absolute_deviation', sa.Float(), nullable=True),
    sa.Column('minimum', sa.Float(), nullable=True),
    sa.Column('standard_deviation', sa.Float(), nullable=True),
    sa.Column('third_quartile', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
    sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_intensities_channel_id'), 'intensities', ['channel_id'], unique=False)
    op.create_index(op.f('ix_intensities_match_id'), 'intensities', ['match_id'], unique=False)
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('center_mass_intensity_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('channel_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('match_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('max_intensity_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.ForeignKeyConstraint(['center_mass_intensity_id'], ['coordinates.id'], ),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
    sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ),
    sa.ForeignKeyConstraint(['max_intensity_id'], ['coordinates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_locations_center_mass_intensity_id'), 'locations', ['center_mass_intensity_id'], unique=False)
    op.create_index(op.f('ix_locations_channel_id'), 'locations', ['channel_id'], unique=False)
    op.create_index(op.f('ix_locations_match_id'), 'locations', ['match_id'], unique=False)
    op.create_index(op.f('ix_locations_max_intensity_id'), 'locations', ['max_intensity_id'], unique=False)
    op.create_table('radial_distributions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bins', sa.Integer(), nullable=True),
    sa.Column('channel_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('match_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('frac_at_d', sa.Float(), nullable=True),
    sa.Column('mean_frac', sa.Float(), nullable=True),
    sa.Column('radial_cv', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
    sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_radial_distributions_channel_id'), 'radial_distributions', ['channel_id'], unique=False)
    op.create_index(op.f('ix_radial_distributions_match_id'), 'radial_distributions', ['match_id'], unique=False)
    op.create_table('textures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channel_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('match_id', perturbation.UUID.UUID(length=16), nullable=True),
    sa.Column('angular_second_moment', sa.Float(), nullable=True),
    sa.Column('contrast', sa.Float(), nullable=True),
    sa.Column('correlation', sa.Float(), nullable=True),
    sa.Column('difference_entropy', sa.Float(), nullable=True),
    sa.Column('difference_variance', sa.Float(), nullable=True),
    sa.Column('scale', sa.Integer(), nullable=True),
    sa.Column('entropy', sa.Float(), nullable=True),
    sa.Column('gabor', sa.Float(), nullable=True),
    sa.Column('info_meas_1', sa.Float(), nullable=True),
    sa.Column('info_meas_2', sa.Float(), nullable=True),
    sa.Column('inverse_difference_moment', sa.Float(), nullable=True),
    sa.Column('sum_average', sa.Float(), nullable=True),
    sa.Column('sum_entropy', sa.Float(), nullable=True),
    sa.Column('sum_variance', sa.Float(), nullable=True),
    sa.Column('variance', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
    sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_textures_channel_id'), 'textures', ['channel_id'], unique=False)
    op.create_index(op.f('ix_textures_match_id'), 'textures', ['match_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_textures_match_id'), table_name='textures')
    op.drop_index(op.f('ix_textures_channel_id'), table_name='textures')
    op.drop_table('textures')
    op.drop_index(op.f('ix_radial_distributions_match_id'), table_name='radial_distributions')
    op.drop_index(op.f('ix_radial_distributions_channel_id'), table_name='radial_distributions')
    op.drop_table('radial_distributions')
    op.drop_index(op.f('ix_locations_max_intensity_id'), table_name='locations')
    op.drop_index(op.f('ix_locations_match_id'), table_name='locations')
    op.drop_index(op.f('ix_locations_channel_id'), table_name='locations')
    op.drop_index(op.f('ix_locations_center_mass_intensity_id'), table_name='locations')
    op.drop_table('locations')
    op.drop_index(op.f('ix_intensities_match_id'), table_name='intensities')
    op.drop_index(op.f('ix_intensities_channel_id'), table_name='intensities')
    op.drop_table('intensities')
    op.drop_index(op.f('ix_edges_match_id'), table_name='edges')
    op.drop_index(op.f('ix_edges_channel_id'), table_name='edges')
    op.drop_table('edges')
    op.drop_index(op.f('ix_correlations_match_id'), table_name='correlations')
    op.drop_index(op.f('ix_correlations_independent_id'), table_name='correlations')
    op.drop_index(op.f('ix_correlations_dependent_id'), table_name='correlations')
    op.drop_table('correlations')
    op.drop_index(op.f('ix_matches_shape_id'), table_name='matches')
    op.drop_index(op.f('ix_matches_pattern_id'), table_name='matches')
    op.drop_index(op.f('ix_matches_object_id'), table_name='matches')
    op.drop_index(op.f('ix_matches_neighborhood_id'), table_name='matches')
    op.drop_index(op.f('ix_matches_center_id'), table_name='matches')
    op.drop_table('matches')
    op.drop_index(op.f('ix_neighborhoods_second_closest_id'), table_name='neighborhoods')
    op.drop_index(op.f('ix_neighborhoods_object_id'), table_name='neighborhoods')
    op.drop_index(op.f('ix_neighborhoods_closest_id'), table_name='neighborhoods')
    op.drop_table('neighborhoods')
    op.drop_index(op.f('ix_quality_image_id'), table_name='quality')
    op.drop_table('quality')
    op.drop_index(op.f('ix_objects_image_id'), table_name='objects')
    op.drop_index(op.f('ix_objects_description'), table_name='objects')
    op.drop_table('objects')
    op.drop_index(op.f('ix_moments_shape_id'), table_name='moments')
    op.drop_table('moments')
    op.drop_index(op.f('ix_images_well_id'), table_name='images')
    op.drop_index(op.f('ix_images_description'), table_name='images')
    op.drop_table('images')
    op.drop_index(op.f('ix_wells_plate_id'), table_name='wells')
    op.drop_index(op.f('ix_wells_description'), table_name='wells')
    op.drop_table('wells')
    op.drop_index(op.f('ix_shapes_center_id'), table_name='shapes')
    op.drop_table('shapes')
    op.drop_index(op.f('ix_plates_description'), table_name='plates')
    op.drop_table('plates')
    op.drop_index(op.f('ix_patterns_description'), table_name='patterns')
    op.drop_table('patterns')
    op.drop_table('coordinates')
    op.drop_index(op.f('ix_channels_description'), table_name='channels')
    op.drop_table('channels')
    ### end Alembic commands ###
