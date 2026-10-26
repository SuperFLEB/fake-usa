<script setup lang="ts">
import {provide, ref} from "vue";
import k from "./keys.ts";
import type {Place} from "@/typedefs/places";

const bucketRef = ref<Place[]>([]);
const intf = {
	add(place: Place) {
		bucketRef.value.push(place);
	},
	remove(index: number) {
		bucketRef.value.splice(index, 1);
	},
	clear() {
		bucketRef.value = [];
	}
};
export type BucketInterface = typeof intf;
provide(k.BUCKET_REF, bucketRef);
provide(k.INTERFACE, intf);
</script>

<template>
	<slot/>
</template>
