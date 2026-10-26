<script setup lang="ts">
import {ref, watch} from "vue";
import {type FIPSCode, STATE_NAME_BY_FIPS, type USStateName} from "@/typedefs/USState.ts";
import useConfigProvider from "@/providers/ConfigProvider/useConfigProvider.ts";
import {FakePlaceNamesQuery, type FakePlaceNamesQueryResult} from "@/sqldata/queries.ts";
import useDb from "@/providers/DBProvider/useDb.ts";
// import useBucket from "@/providers/BucketProvider/useBucket .ts";
import type {Place} from "@/typedefs/places";
import makePlace from "@/util/makePlace.ts";

const {stateFIPSCode} = useConfigProvider();
const stateName = ref<USStateName|null>(null);
const placeNamesResult = ref<FakePlaceNamesQueryResult[]>([]);
const db = useDb();
// const { bucketRef, interface: bucketInterface } = useBucket();

const emit = defineEmits<{
	(e: "pickItem", place: Place): void
}>();

function refresh() {
	stateName.value = STATE_NAME_BY_FIPS[stateFIPSCode.value];
	const query = new FakePlaceNamesQuery(db(), {stateFIPSCode: stateFIPSCode.value as FIPSCode, count: 20});
	placeNamesResult.value = query.execute();
}

function pick(placeQueryResult: FakePlaceNamesQueryResult) {
	emit("pickItem", makePlace(db(), {
		fips: stateFIPSCode.value,
		name: placeQueryResult.featureName,
		teams: [],
		zips: [],
		phone: [],
		callsigns: []
	}));
}

watch(stateFIPSCode, refresh, { immediate: true });

</script>

<template>
	<ul class="placeNames">
		<li :class="{placeName: true, isSettlement: result.isSettlement, isNotSettlement: !result.isSettlement}" v-for="(result, index) in placeNamesResult" :key="index">
			<button @click="pick(result)">{{ result.featureName }}, {{ stateName }}</button>
		</li>
		<li class="keepDriving">
			<button @click="refresh">Keep<br />Driving</button>
		</li>
	</ul>
</template>

<style scoped>
	@import url('https://fonts.googleapis.com/css2?family=Overpass:ital,wght@0,100..900;1,100..900&display=swap');
	.placeNames {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		gap: 1rem;

		list-style: none;
		margin: 0;
		padding: 0;

		font-family: "Overpass", sans-serif;
		font-weight: 800;
		font-size: 1.25rem;

		button {
			background-color: transparent;
			border: none;
			color: inherit;
			font: inherit;
			text-transform: inherit;
			cursor: pointer;
		}
	}
	.placeName, .keepDriving {
		width: 10em;
		margin: 0;
		padding: 1em;
		position: relative;

		align-content: center;
		text-align: center;

		border-radius: 1em;
		border: 1px outset #060;
		box-shadow: 0.25em 0.25em 0.25em rgba(0, 0, 0, 0.4);

		outline: 3px solid currentColor;
		outline-offset: -0.5em;
	}

	.placeName {
		background-color: #363;
		color: #fff;

		&.isNotSettlement {
			background-color: #446;
			border-color: #446;
		}

		&:before {
			content: "Welcome To";
			display: block;
			font-family: serif;
			font-size: 0.5em;
			font-weight: 400;
			text-transform: uppercase;
			letter-spacing: 0.2em;
			margin-bottom: 0.5em;
		}
	}

	.keepDriving {
		background-color: #fa0;
		border-color: #fa0;
		color: #000;
		text-transform: uppercase;
		font-size: 1.25em;
	}
</style>