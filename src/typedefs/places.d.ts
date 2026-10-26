import type {FIPSCode} from "./USState.ts"

export type Zip = {
	number: number;
	level: 0 | 1 | 2 | 3;
}

export type PhoneNumberPrefix = {
	// ---------------- For (123)456-7xxx
	//                  --- --------------
	block_start: number //   123 456 7000 = 1234567000
	npanxxx: number;    //   123 456 7... = 1234567
	npanxx: number;     //   123 456 .... = 123456
	nxxx: number;       //   ... 456 7... = 4567
	//                  --- --------------
	npa: number;        //   123 ... .... = 123
	nxx: number;        //   ... 456 ....  = 456
	x: number;          //   ... ... 7...  = 7
}

export type TeamLevel = "PRO" | "COLLEGE" | "SECONDARY";
export type Sport = "FOOTBALL" | "BASKETBALL" | "BASEBALL" | "HOCKEY" | "SOCCER";

export type Team = {
	level?: TeamLevel;
	sport?: Sport;
	name: string;
}

export type Place = {
	fips: FIPSCode;
	name: string;
	region?: string;
	subregion?: string;
	callsigns: string[];
	teams: Team[];
	zips: Zip[];
	phone: Nxxx[];
}
