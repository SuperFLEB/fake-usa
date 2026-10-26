# Fake USA

Based loosely on my prior Fake USA data compilation, this is a tool that allows you to
pick from countless plausible but fake place names by showing you names that exist, just
not in the state you selected.

It also generates fake ZIP codes and fake phone number blocks, for all your making-things-up
needs.

## Usage

You can use it online by visiting the GitHub Pages site, or build it yourself and run it locally.
It runs in the browser and works entirely offline, using a local SQLite database to fetch data.
It comes with a pre-populated database, as well as most of the tools to pull down fresh data.

> TODO: Add actual build instructions. It's a Vue 3 app built with Vite, so in short, just run `pnpm install` and `pnpm dev` to get it going.

## Status and Future Plans

This is still in development. I'm cleaning up and migrating features from a prior, unpublished version,
so here's what to look out for, and what to look for in upcoming versions:

- Persistence across reloads.
- Ability to compile and save a list of generated places. More ability to tweak the generated places.
- ZIP code listings that allow you to pick "how fake" you want. Get only ZIPs that are completely unused,
  ones that are used internally by the USPS, or ones that may be valid but not for geographical addresses.
  For now, check your ZIP codes before you use them.


