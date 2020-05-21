from data_b.db import add_user
from data_b.db import get_karma
from data_b.db import update_karma
from data_b.db import isCreate

# add_user(user_id=1344232, karma=0)
# add_user(user_id=2333333, karma=5)


print(isCreate(user_id=233333))
print(type(get_karma(user_id=2333333)))