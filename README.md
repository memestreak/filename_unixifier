# Filename Unixifier

This tool renames files to be UNIX idiomatic, removing spaces, etc.

## Usage
```sh
filename_unixifier.py [--noop] [--ipython] [filename ...]

--noop, -n    : Do not perform any writes
--ipython, -i : Just drop into an IPython REPL for debugging
```

### Example

```sh
# Assuming we've just ripped a compact disc, fix the output filenames.
$ filename_unixifier.py *
"01 - A Rush and a Push and the Land Is Ours.flac" --> "01-a_rush_and_a_push_and_the_land_is_ours.flac": ✅
"02 - I Started Something I Couldn’t Finish.flac" --> "02-i_started_something_i_couldnt_finish.flac": ✅
"03 - Death of a Disco Dancer.flac" --> "03-death_of_a_disco_dancer.flac": ✅
"04 - Girlfriend in a Coma.flac" --> "04-girlfriend_in_a_coma.flac": ✅
"05 - Stop Me If You Think You’ve Heard This One Before.flac" --> "05-stop_me_if_you_think_youve_heard_this_one_before.flac": ✅
"06 - Last Night I Dreamt That Somebody Loved Me.flac" --> "06-last_night_i_dreamt_that_somebody_loved_me.flac": ✅
"07 - Unhappy Birthday.flac" --> "07-unhappy_birthday.flac": ✅
"08 - Paint a Vulgar Picture.flac" --> "08-paint_a_vulgar_picture.flac": ✅
"09 - Death at One’s Elbow.flac" --> "09-death_at_ones_elbow.flac": ✅
"10 - I Won’t Share You.flac" --> "10-i_wont_share_you.flac": ✅
```

## Reference

See also the command line utility `rename` which has some overlap with
this tool.
