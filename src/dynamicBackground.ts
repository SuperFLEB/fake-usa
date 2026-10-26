import shuffleArrayInPlace from "@/util/shuffleArrayInPlace.ts";
import {STATE_BY_FIPS} from "@/typedefs/USState.ts";
import backgroundImage from "@/assets/states-background.svg";

export default async function dynamicBackground(): Promise<URL> {
	return await fetch(backgroundImage)
		.then(response => response.text())
		.then(svgText => {
			const states = shuffleArrayInPlace([...Object.values(STATE_BY_FIPS), ...Object.values(STATE_BY_FIPS), ...Object.values(STATE_BY_FIPS), ...Object.values(STATE_BY_FIPS)]);
			const useStatements = states.map((state, index) => {
				const x = index % 16 * 100;
				const y = Math.floor(index / 16) * 100;
				const wh = 150;
				const color = `hsla(${Math.random() * 360}, 60%, 30%, 0.05)`;
				return `<use href="#${state}" width="${wh}" height="${wh}" x="${x}" y="${y}" transform="rotate(${Math.random() * 60 - 30})" transform-origin="${x+wh/2} ${y+wh/2}" stroke="${color}"/>`;
			}).join("");
			svgText = svgText.replace("<!-- instances go here -->", useStatements);
			return new URL(URL.createObjectURL(new Blob([svgText], {type: "image/svg+xml"})));
		});
}
