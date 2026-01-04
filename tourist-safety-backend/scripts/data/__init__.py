# All India Districts Data - Combined
from scripts.data.north_india import NORTH_INDIA_DISTRICTS
from scripts.data.west_central_india import WEST_CENTRAL_INDIA_DISTRICTS
from scripts.data.south_india import SOUTH_INDIA_DISTRICTS
from scripts.data.east_india import EAST_NORTHEAST_INDIA_DISTRICTS
from scripts.data.northeast_rajasthan import NORTHEAST_RAJASTHAN_DISTRICTS

# Combine all districts
ALL_DISTRICTS = (
    NORTH_INDIA_DISTRICTS +
    WEST_CENTRAL_INDIA_DISTRICTS +
    SOUTH_INDIA_DISTRICTS +
    EAST_NORTHEAST_INDIA_DISTRICTS +
    NORTHEAST_RAJASTHAN_DISTRICTS
)

# Count summary
print(f"Total districts loaded: {len(ALL_DISTRICTS)}")
