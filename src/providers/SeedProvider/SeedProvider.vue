<script setup lang="ts">
import {provide, ref} from "vue";
import k from "./keys.ts";

const intf = {
	getNextRandom(key: string): number {
		return 4;
	},
	getIndexedRandom(key: string, index: number) {

	},
};
export type SeedProviderInterface = typeof intf;

provide(k.INTERFACE, intf);
</script>

<template>
<slot />
</template>
