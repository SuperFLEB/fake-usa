<script setup lang="ts">
import useBucket from "@/providers/BucketProvider/useBucket .ts";
import {STATE_BY_FIPS} from "@/typedefs/USState.ts";
import type {Place} from "@/typedefs/places";

const emit = defineEmits<{
	(e: "pickItem", place: Place): void
}>();
const {bucketRef, interface: bucketInterface} = useBucket();

function emitPick(place: Place) {
	emit("pickItem", place);
}
</script>

<template>
	<ul>
		<li v-for="place in bucketRef">
			<button @click="emitPick(place)">{{ place.name }}, {{ STATE_BY_FIPS[place.fips] }}</button>
		</li>
	</ul>
</template>

<style scoped>

</style>