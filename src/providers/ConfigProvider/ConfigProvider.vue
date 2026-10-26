<script setup lang="ts">

import {provide, ref} from "vue";
import {FIPS_BY_STATE_ABBR, type FIPSCode, type USStateAbbreviation} from "@/typedefs/USState.ts";
import k from "./keys.ts";
import debouncedRef from "@/util/debouncedRef.ts";

const stateFIPSCode = ref<FIPSCode | null>(null);
const nameFilter = debouncedRef<string | null>(null, 500);

const intf = {
	setState: (abbrOrFIPSCode: USStateAbbreviation | FIPSCode) => {
		stateFIPSCode.value = (typeof abbrOrFIPSCode === "number") ? abbrOrFIPSCode : FIPS_BY_STATE_ABBR[abbrOrFIPSCode];
	},
	setNameFilter: (_nameFilter: string, immediate: boolean = false) => {
		if (immediate) {
			nameFilter.value = _nameFilter;
			return;
		}
	}
};
export type ConfigProviderInterface = typeof intf;

provide(k.STATE_FIPS_CODE, stateFIPSCode);
provide(k.NAME_FILTER, nameFilter);
provide(k.INTERFACE, intf);
</script>

<template>
<slot />
</template>
