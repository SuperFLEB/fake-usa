<script setup lang="ts">
import PlaceList from "@/components/PlaceList.vue";
import GlobalUsStatePicker from "@/components/GlobalUsStatePicker.vue";
import Bucket from "@/components/Bucket.vue";
import type {Place} from "@/typedefs/places";
import {onMounted, onUnmounted, ref, useTemplateRef} from "vue";
import Detail from "@/components/Detail.vue";
import {Pane, Splitpanes} from "splitpanes";
import "splitpanes/dist/splitpanes.css";
import useConfigProvider from "@/providers/ConfigProvider/useConfigProvider.ts";
import NoPlaceList from "@/components/NoPlaceList.vue";

const detailItemRef = ref<Place | null>(null);
const narrowMql = window.matchMedia("(max-width: 1119.9px)");
const narrow = ref(narrowMql.matches);

const detailPaneRef = useTemplateRef('detailPane');

function resizeListener(e: MediaQueryListEvent) {
	narrow.value = e.matches;
}

function setDetailItem(place: Place) {
	detailItemRef.value = place;
	if (narrow.value && detailPaneRef.value) {
		detailPaneRef.value.scrollIntoView(true);
	}
}

onMounted(() => {
	narrowMql.addEventListener("change", resizeListener);
});

onUnmounted(() => {
	narrowMql.removeEventListener("change", resizeListener);
});

const {stateFIPSCode} = useConfigProvider();
</script>

<template>
	<h1><span class="welcome">Welcome to</span> Fake
		<GlobalUsStatePicker/>
	</h1>

	<splitpanes :vertical="!narrow" :horizontal="narrow" v-if="stateFIPSCode">
		<pane size="70">
			<PlaceList @pickItem="setDetailItem"/>
		</pane>
		<pane>
			<splitpanes horizontal>
				<pane>
					<Detail :place="detailItemRef ?? undefined"/>
					<a id="detail-pane" ref="detailPane" />
				</pane>
				<pane>
					<Bucket @pickItem="setDetailItem"/>
				</pane>
			</splitpanes>
		</pane>
	</splitpanes>

	<NoPlaceList v-else/>

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

@media screen and (max-width: 1119.9px) {
	h1 {
		font-size: 3em;
	}
}

a#detail-pane {
	width: 0;
	height: 0;
	margin: 0;
	padding: 0;
	border: 0 none;
	visibility: hidden;
}

</style>

