<script setup lang="ts">
import type {Place} from "@/typedefs/places";
import {STATE_BY_FIPS, STATE_NAME_BY_FIPS} from "@/typedefs/USState.ts";
import {computed, onMounted, ref, watch} from "vue";
import useConfigProvider from "@/providers/ConfigProvider/useConfigProvider.ts";
import arrayPickRandom from "@/util/arrayPickRandom.ts";

type Props = { place?: Place };
const props = defineProps<Props>();

const isTV = ref(false);
const channel = ref("");
const connector = ref("");
const placeBeforeTeam = ref(false);

const placeGreeting = ref(["", ""]);
watch(() => [props.place], () => {
	placeGreeting.value = arrayPickRandom([
		["Welcome to", ""],
		["", "welcomes you"],
		["Experience the splendor of", ""],
		["Greetings from", ""],
		["Experience lovely", ""],
		["Explore", ""],
		["", "is waiting for you"],
		["There's plenty to see in", ""],
		["Find your getaway in", ""],
		["", "is calling"],
		["Imagination awaits in", ""]
	]);

	isTV.value = Math.random() > 0.5;
	if (isTV.value) {
		channel.value = `TV ${Math.floor(Math.random() * 98) + 2}`;
	} else {
		const amfm = Math.random() > 0.5;
		if (amfm) {
			const freq = (Math.floor(Math.random() * 99) * 2 + 881) / 10;
			channel.value = `${freq} FM`;
		} else {
			const freq = (Math.floor(Math.random() * 117) + 53) * 10;
			channel.value = Math.random() > 0.5 ? `AM ${freq}` : `${freq} AM`;
		}
	}

	connector.value = arrayPickRandom([
		"",
		"live from",
		"coming to you from",
		"in",
		"from",
		"broadcasting from",
	]) + " ";

	placeBeforeTeam.value = Math.random() > 0.5;
}, {immediate: true});

const {stateFIPSCode} = useConfigProvider();
const sportsballs = ["⚽", "⚾", "🥎", "🏀", "🏐", "🏈", "🏉", "🏏", "🏑", "🏒", "🥍", "🥅"];

</script>

<template>
	<template v-if="props.place">
		<h3>
			<span class="secondary-title-text">{{ placeGreeting[0] }}</span>
			{{ props.place.name }}, {{ STATE_NAME_BY_FIPS[props.place.fips] }}{{placeGreeting[1] ? '' : '.'}}
			<span class="secondary-title-text" v-if="placeGreeting[1]">{{ placeGreeting[1] }}.</span></h3>
		<ul class="detail-list">
			<li class="zips">
				<ul>
					<li v-for="zip in props.place.zips">{{ String(zip.number).padStart(5, "0") }}</li>
				</ul>
			</li>
			<li class="phones">
				<ul>
					<li v-for="phone in props.place.phone">({{ phone.npa }}) {{ phone.nxx }}-{{ phone.x }}xxx</li>
				</ul>
			</li>
			<li class="callsigns">
				<ul>
					<li v-for="radio in props.place.callsigns">{{ radio }}</li>
				</ul>
			</li>
			<li class="teams">
				<ul>
					<li v-for="team in props.place.teams" :style="{ '--sport-emoji': `'${arrayPickRandom(sportsballs)}'` }">{{ team.name }}</li>
				</ul>
			</li>
		</ul>

		<div class="blurb-icon">{{ isTV ? "📺" : "📻" }}</div>
		<div class="blurb">
			You're {{ isTV ? "watching" : "listening to" }} {{ props.place.callsigns[0] }} {{ channel }} {{ connector }}
			{{ props.place.name }}. We're {{ props.place.subregion }} {{ props.place.region }}'s home for news, weather,
			and
			<template v-if="placeBeforeTeam">{{ props.place.name }}</template>
			{{ props.place.teams[0]!.name }} {{ (props.place.teams[0]!.sport ?? "sports").toLowerCase() }}.
		</div>
	</template>
	<template v-else>
		<p class="placeholder">
			<span class="secondary-title-text">{{ placeGreeting[0] }}</span>
			Fake {{ STATE_NAME_BY_FIPS[stateFIPSCode] }}{{ placeGreeting[1] ? "" : "." }}
			<span class="secondary-title-text" v-if="placeGreeting[1]">{{ placeGreeting[1] }}.</span>
			{{ ' ' }}
			<span class="secondary-title-text">Select a place name for more ideas.</span>
		</p>
	</template>
</template>

<style scoped>
.detail-list {
	list-style: none;
	padding: 0;
	font-size: 1.2rem;
}

h3, .placeholder {
	font-family: 'Caprasimo', sans-serif;
	font-size: 3rem;
	font-weight: 400;
	margin: 0 0 0.5em 0;

	.secondary-title-text {
		-webkit-text-stroke: 2px currentColor;
		-webkit-text-fill-color: transparent;
	}
}

.blurb {
	font-family: "Road Rage", sans-serif;
	font-size: 3rem;
	margin-left: 5.5rem;
	line-height: 1;
}

.blurb-icon {
	font-size: 4rem;
	float: left;
}

.detail-list > li {
	& > ul {
		display: block;
		list-style: none;
		padding: 0;
		margin: 0 0 1em 0;

		& > li {
			position: relative;
			display: inline-block;
			margin: 0 0.5em;
			padding-left: 1.5em;

			&::before {
				position: absolute;
				top: 0;
				left: 0;
			}
		}
	}

	&.zips li::before {
		content: "📫";
	}

	&.phones li::before {
		content: "☎️";
	}

	&.callsigns li::before {
		content: "📡";
	}

	&.teams li::before {
		content: var(--sport-emoji);
	}
}
</style>