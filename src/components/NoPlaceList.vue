<template>
<div class="container">
	<p class="intro">
		Telling a tall tale or spinning a story? Need a place to put it? Just pick a state from the dropdown!
	</p>

	<p>
		If you're tired of wracking your brain only to come up with a fake place that sounds like you
		only wracked your brain to think of it, this is the tool for you. It gives you a selection of
		place names that are both realistic and completely fabricated. How? It's easy! Start with a list
		of every place name in the United States, then pick a list of everywhere that <em>isn't</em> in
		the state you selected. Real name, fake place!
	</p>

	<p>
		Want more? You also get call letters for the local radio or TV station, plausible ZIP codes, and
		phone numbers. (Selected the same way&mdash; by taking the plausible ones and subtracting the real ones.)
	</p>
	<p>
		<em>Developer's note:</em> Call letters are made by literally iterating through every Kxxx and Wxxx
		combination and throwing out existing ones from an FCC list. This means that you may run into an offensive
		word. It's randomly generated. It's nothing personal. Just laugh it off and hit the button again for a new one.
	</p>
	<p>
		<em>Developer's other note:</em> This whole thing is in active development and may have bugs. Most notably,
		the phone number and ZIP code selections are still in development, and might not be accurate just yet.
		Check your selection with a Web search to be sure the phone number or ZIP code you choose is actually unused.
	</p>

	<h3>Coming Soon:</h3>
	<ul>
		<li>Pick place names by how common or rare they are.</li>
		<li>ZIP code "fakeness" tuning for more options that fit your needs.</li>
		<li>Change details and save place profiles.</li>
	</ul>
</div>
</template>

<style scoped>
.container {
	max-width: 70%;
	margin: 0 auto;
}

.intro, h2, h3 {
	font-family: 'Caprasimo', sans-serif;
	font-size: 4em;
}

h3 {
	font-size: 2em;
}
</style>