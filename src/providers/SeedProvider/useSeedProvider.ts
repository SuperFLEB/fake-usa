import {inject, type Ref} from "vue";
import k from "./keys.ts";
import {ComposableOutOfContextError} from "@/errors.ts";
import type { SeedProviderInterface } from "./SeedProvider.vue";

export default function useSeedProvider() {
	const intf = inject<SeedProviderInterface>(k.INTERFACE);

	if (!(intf && 1)) throw new ComposableOutOfContextError("useSeedProvider can't be used outside a SeedProvider");

	return { interface: intf };
}