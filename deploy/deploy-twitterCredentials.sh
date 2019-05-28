#!/bin/bash

#!/bin/bash

echo "Note: first, lpass login [username]"
lpass status


mkdir -p ~/.secrets

#twitter auth (vlan200)
lpass show --notes "Veclas/twitter/vlan200" > ~/.secrets/twitter

