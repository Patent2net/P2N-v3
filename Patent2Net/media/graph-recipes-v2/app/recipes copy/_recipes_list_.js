/* Recipes list */
angular.module('graphrecipes.recipes_list', [])
.constant('recipesList', [
	{
		'name': 'Attributes stats',
		'desc': 'Discover stats based on the networks attributes',
		'file': 'fulldiagnostic.js'
	},
	{
		'name': 'Draw graph',
		'desc': 'Dynamic visualization of your graph',
		'file': 'sigma.js'
	},
	{
		'name': 'Partition Analysis',
		'desc': 'Additional details on a categorical attribute',
		'file': 'partition.js'
	},
	{
		'name': 'Betweenness Centrality',
		'desc': 'Add that metric to your node and edge attributes',
		'file': 'betweenness.js'
	}
])
