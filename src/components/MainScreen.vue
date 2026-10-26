<script setup lang="ts">
import PlaceList from "@/components/PlaceList.vue";
import GlobalUsStatePicker from "@/components/GlobalUsStatePicker.vue";
import Bucket from "@/components/Bucket.vue";
import type {Place} from "@/typedefs/places";
import {ref} from "vue";
import Detail from "@/components/Detail.vue";
import {Pane, Splitpanes} from "splitpanes";
import "splitpanes/dist/splitpanes.css";
import useConfigProvider from "@/providers/ConfigProvider/useConfigProvider.ts";
import NoPlaceList from "@/components/NoPlaceList.vue";

const detailItemRef = ref<Place | null>(null);

function setDetailItem(place: Place) {
	detailItemRef.value = place;
}

const {stateFIPSCode} = useConfigProvider();
</script>

<template>
	<h1><span class="welcome">Welcome to</span> Fake
		<GlobalUsStatePicker/>
	</h1>

	<splitpanes vertical v-if="stateFIPSCode">
		<pane size="70">
			<PlaceList @pickItem="setDetailItem"/>
		</pane>
		<pane>
			<splitpanes horizontal>
				<pane>
					<Detail :place="detailItemRef ?? undefined"/>
				</pane>
				<pane>
					<Bucket @pickItem="setDetailItem"/>
				</pane>
			</splitpanes>
		</pane>
	</splitpanes>

	<NoPlaceList v-else />

</template>

<style scoped>
.welcome {
	-webkit-text-stroke: 2px currentColor;
	-webkit-text-fill-color: transparent;
}

h1, h2, h3, h4, h5, h6 {
	font-family: 'Caprasimo', sans-serif;
	font-weight: normal;
}

h1 {
	font-size: 4em;
	text-align: center;
}

</style>

