import type {PhoneNumberPrefix} from "@/typedefs/places";

export default function toPhoneNumberPrefix(npanxxx: number): PhoneNumberPrefix {
	return {
		block_start: npanxxx * 1000,
		npanxxx,
		npanxx: Math.floor(npanxxx / 10),
		nxxx:   Math.floor(npanxxx % 10000),

		npa: Math.floor(npanxxx / 10000),
		nxx: Math.floor(npanxxx % 10000 / 10),
		x: npanxxx % 10,
	};
}