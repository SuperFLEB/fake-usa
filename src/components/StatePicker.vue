<script setup lang="ts">
import {FIPS_BY_STATE_NAME, type FIPSCode} from "@/typedefs/USState.ts";
const model = defineModel<FIPSCode | null>();
type Props = { nothingText?: string, hideNothing?: boolean };
const props = withDefaults(defineProps<Props>(), { nothingText: "USA", hideNothing: true });

</script>

<template>
<span class="state-picker-wrapper">
	<select v-model="model">
		<option :value="null" v-if="hideNothing && model === null">{{ nothingText }}</option>
		<option v-for="(fips, state) in FIPS_BY_STATE_NAME" :value="fips">{{state}}</option>
	</select>
</span>
</template>

<style scoped>
	.state-picker-wrapper {
		border: 3px solid color-mix(in srgb, currentColor 15%, transparent);
		border-radius: 0.5em;
		padding: 0.125em 0.25em;

		position: relative;
		&::after {
			content: "▾";
			pointer-events: none;
			position: absolute;
			top: 0.25em;
			right: 0;
		}
	}

	select {
		appearance: none;
		color: inherit;
		background: transparent;
		border: 0 none;
		font: inherit;
		field-sizing: content;
		padding-right: 1em;

		option {
			font-size: 1rem;
		}
	}
</style>