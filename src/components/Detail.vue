<script setup lang="ts">
import type {Place} from "@/typedefs/places";
import {STATE_BY_FIPS, STATE_NAME_BY_FIPS} from "@/typedefs/USState.ts";
import {computed, onMounted, ref, watch} from "vue";

type Props = { place?: Place };
const props = defineProps<Props>();

const isTV = ref(false);
const channel = ref("");
const connector = ref("");

watch(() => props.place, () => {
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

	connector.value = [
		"",
		"live from",
		"coming to you from",
		"in",
		"from",
		"broadcasting from",
	].at(Math.floor(Math.random() * 6)) + " ";
}, {immediate: true});

</script>

<template>
	<template v-if="props.place">
		<ul class="detail-list">
			<li class="name">{{ props.place.name }}, <span class="state-name">{{
					STATE_BY_FIPS[props.place.fips]
				}}</span></li>
			<li class="zips">
				<ul class="sublist zips">
					<li v-for="zip in props.place.zips">{{ String(zip.number).padStart(5, "0") }}</li>
				</ul>
			</li>
			<li class="phones">
				<ul class="sublist phones">
					<li v-for="phone in props.place.phone">({{ phone.npa }}) {{ phone.nxx }}-{{ phone.x }}xxx</li>
				</ul>
			</li>
		</ul>

		<div class="blurb-icon">{{ isTV ? "📺" : "📻" }}</div>
		<div class="blurb">
			You're {{ isTV ? "watching" : "listening to" }} {{ props.place.callsigns[0] }} {{ channel }} {{ connector }}
			{{ props.place.name }}. We're {{ props.place.subregion }} {{ props.place.region }}'s home for news, weather, and
			{{ props.place.teams[0]!.name }} {{ (props.place.teams[0]!.sport ?? "sports").toLowerCase() }}.
		</div>

	</template>
</template>

<style scoped>
.detail-list {
	list-style: none;
	padding: 0;
	font-size: 1.2rem;
}

li.name {
	font-family: 'Caprasimo', sans-serif;
	font-size: 3rem;
	margin: 0.5em 0;

	.state-name {
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

.sublist {
	display: inline;
	list-style: none;
	padding: 0;
	margin: 0;

	li {
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

	&.zips li::before {
		content: "📫";
	}
	&.phones li::before {
		content: "☎️";
	}

}
</style>