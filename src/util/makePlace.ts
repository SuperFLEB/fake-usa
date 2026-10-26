import type {PhoneNumberPrefix, Place, Sport, Team, TeamLevel, Zip} from "@/typedefs/places";
import {type FIPSCode, STATE_NAME_BY_FIPS} from "@/typedefs/USState.ts";
import {CallsignQuery, PhoneQuery, RegionQuery, TeamQuery, ZipQuery} from "@/sqldata/queries.ts";
import type {Database} from "@sqlite.org/sqlite-wasm";

function getRandomRegion(db: Database, fips: FIPSCode): [string, string] {
	const results = new RegionQuery(db, {fips}).execute();
	if (!results?.length) return [STATE_NAME_BY_FIPS[fips], ""];
	const randomIndex = Math.floor(Math.random() * results.length);
	return [results[randomIndex]!.region, results[randomIndex]!.subregion];
}

function getRandomCallsigns(db: Database, fips: FIPSCode, count = 1): string[] {
	const query = new CallsignQuery(db, {fips, count});
	return query.execute()!.map(row => row.callsign);
}

function getRandomTeams(db: Database, count = 1): Team[] {
	const query = new TeamQuery(db, {count});
	const names = query.execute().map(row => row.name);

	return names.map(name => {
		const level = (["PRO", "COLLEGE", "SECONDARY"])[Math.floor(Math.random() * 3)] as TeamLevel;
		const sport = (["FOOTBALL", "BASKETBALL", "BASEBALL", "HOCKEY", "SOCCER"])[Math.floor(Math.random() * 5)] as Sport;
		return {level, sport, name};
	});
}

function getRandomNxxx(db: Database, count = 1): PhoneNumberPrefix[] {
	const query = new PhoneQuery(db, {count});
	return query.execute();
}

function getRandomZip(db: Database, fips: FIPSCode, count = 1): Zip[] {
	const query = new ZipQuery(db, {fips, count, level: 0});
	return query.execute();
}

export default function makePlace(db: Database, place: Place, count: number = 10): Place {
	if (!place.region) {
		const region = getRandomRegion(db, place.fips);
		place.region = region[0];
		place.subregion = region[1];
	}

	if (!place.callsigns?.length) {
		place.callsigns = getRandomCallsigns(db, place.fips, count);
	}

	if (!place.teams?.length) {
		place.teams = getRandomTeams(db, count);
	}

	if (!place.zips?.length) {
		place.zips = getRandomZip(db, place.fips, count);
	}

	if (!place.phone?.length) {
		place.phone = getRandomNxxx(db, count);
	}

	return place;
}