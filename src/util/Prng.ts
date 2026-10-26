const GOLDEN_RATIO_32 = 0x9e3779b9;
const MAGIC_1 = 0x21f0aaad;
const MAGIC_2 = 0x735a2d97;
const MAX_32 = 0xFFFFFFFF
const BIT_33 = 0x100000000;

export type RandomNumberArray = number[] & { seed: number, iteration: number };

function splitMix32(seed: number, iteration: number, count: number = 1): number[] {
	let s = (seed + Math.imul(iteration, GOLDEN_RATIO_32)) & MAX_32
	const output = [];
	for (let subIter = 0; subIter < count; subIter++) {
		s = (s + GOLDEN_RATIO_32) | 0;

		let t = s ^ (s >>> 16);
		t = Math.imul(t, MAGIC_1);
		t = t ^ t >>> 15;
		t = Math.imul(t, MAGIC_2);

		output.push(((t ^ (t >>> 15)) >>> 0) / BIT_33);
	}
	return output;
}

export default class Prng {
	private _seed: number;
	private _iteration: number = 0;

	get seed(): number {
		return this._seed;
	}

	get iteration(): number {
		return this._iteration;
	}

	set iteration(iteration: number) {
		this._iteration = iteration;
	}

	public reset(seed?: number, iteration: number = 0) {
		this._seed = (seed ?? Math.random() * BIT_33) | 0;
		this._iteration = iteration;
	}

	public getRandoms(iteration: number, count: number = 1): RandomNumberArray {
		const numbers = splitMix32(this._seed, iteration, count);
		Object.defineProperty(numbers, "seed", { value: this._seed });
		Object.defineProperty(numbers, "iteration", { value: iteration });
		return numbers as RandomNumberArray;
	}

	public randoms(count: number = 1): RandomNumberArray {
		const numbers = this.getRandoms(this._iteration, count);
		this._iteration += count;
		return numbers;
	}

	public random(): number {
		return this.randoms()[0] as number;
	}

	constructor(seed?: number) {
		this._seed = (seed ?? (Math.random() * BIT_33)) | 0;
	}
}
