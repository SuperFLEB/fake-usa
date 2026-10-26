import {inject, type Ref} from "vue";
import k from "./keys.ts";
import {ComposableOutOfContextError} from "@/errors.ts";
import type {BucketInterface} from "./BucketProvider.vue";
import type {Place} from "@/typedefs/places";

export default function useBucket() {
	const intf = inject<BucketInterface>(k.INTERFACE);
	const bucketRef = inject<Ref<Place[]>>(k.BUCKET_REF);
	if (!(intf && bucketRef)) throw new ComposableOutOfContextError("useBucket can't be used outside a BucketProvider");
	return {interface: intf, bucketRef};
}