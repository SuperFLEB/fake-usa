import {inject, type Ref} from "vue";
import k from "./keys.ts";
import {ComposableOutOfContextError} from "@/errors.ts";
import type { ConfigProviderInterface } from "./ConfigProvider.vue";
import type {FIPSCode} from "@/typedefs/USState.ts";

export default function useConfigProvider() {
	const intf = inject<ConfigProviderInterface>(k.INTERFACE);
	const stateFIPSCode = inject<Ref<FIPSCode>>(k.STATE_FIPS_CODE);
	const nameFilter = inject<Ref<string>>(k.NAME_FILTER);

	if (!(intf && stateFIPSCode && nameFilter)) throw new ComposableOutOfContextError("useConfigProvider can't be used outside a ConfigProvider");

	return { interface: intf, stateFIPSCode, nameFilter };
}