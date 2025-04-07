# comps_24_25

NOTE: To run battles with the Pokemon-Showdown simulator (which we use for q-learning), enter the following commands into your terminal before running the q-learning agent notebook:

git clone https://github.com/smogon/pokemon-showdown.git
cd pokemon-showdown
npm install
cp config/config-example.js config/config.js
node pokemon-showdown start --no-security

To run Minimax download the minimax and teams file, and simply run the Minimax file. Right now there is an instance of a battle set up within it and commented out code to automate many battles. Additionally, it needs the edited Poke-Battle-Sim so that deepCopy works.

Additionally, src, data, poke-data, and pokemon-showdown aren't necessary
