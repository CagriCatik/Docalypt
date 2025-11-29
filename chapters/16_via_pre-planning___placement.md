# Via Pre-Planning & Placement



What we can do and what I typically do generally and this is not just for ground nets. This is for power or anywhere where I might think I I might need a via is I do my via pre-placement. If you just start routting right away laying down tracks and whatnot you'll very quickly see once you need to start adding vas later that there going to be loads of issues.

You're going to have to rearrange tracks, rearrange components, rearrange VAS. So that's why as far as I can, I also try to pre-plan my VA before I lay any traces out. A rule of thumb is that if we have for instance a ground plane as we do here on the second layer, that for every ground pad we see here, we want at least one via very close to that pad, not in the pad, but adjacent to the pad that goes to ground.

Later on we will then link that up either with another polygon paw on the top layer or with wide short traces that we have nice low inductance low impedance ground connections. The way I can place a via is either go to the right hand side click on that little place icon or press control shift X on my keyboard.

You also have to of course choose your correct via size and I'll just choose our standard or our predefined 7.3 mm via. Then click on the V tool and you can see our V is now free to move. I want to change my grid. It's a bit large at the moment. So I'm going to press N and move down to 0.25 mm. So for instance for C12 I definitely do not want to place the VN pad.

There are very good reasons for doing so, but typically that requires a different PCB process manufacturing process or rather an additional PCB manufacturing process which you should avoid for most boards unless you have very good reason to do so. So the ground via I like to place just outside the copper pads area. For instance, here would be a good spot or even just below.

Remember our ground of pin 7 is down there. So I kind of want to have my ground connections facing the shortest loop area. So in this case I would probably place my ground V like so. It's not connected yet but it's just in a way a symbolic representation that we need to connect this and I'm pre-placing my VA. Same for the ground here. I'm just going to place it slightly outside of the pad like so.

And I'm going to repeat that process with a minimum of one ground via per ground pad. Ground v in parallel assuming the correct connections can reduce the impedance. So that's why often times it can pay off to actually have multiple ground v around the pad. for instance, like so.

But as a bare minimum, I'd suggest just doing one grand via per pad just to start off with. And if you have space later on, add more in. Now, of course, for higher power designs, higher current designs, you will have to use multiple VA. If you need to transition through layers or if you need a low inductance, low low impedance ground connection, then of course you will have to use parallel VA.

But for a simple board like this, a simple design, go with a rule of thumb, one ground via per pad. Place close to the pad, but not in the pad. So, let me just add the remaining vas. And I hope you do the same on your end. And here I've now placed at least one via per pad fairly roughly.

You might have to move these around as we get through to routing, of course. But again, just slightly outside the pad for the most part. Sometimes I've just, you know, gone a bit crazy and added a few more just around. And we'll come to stitching v later on when we do a top polygon paw. But for instance, for example, for power components, I typically add even more than one via again just to reduce the overall inductance of that connection. The VA is in place, they actually can strain how we route out as well.

This will block off some areas which we can't go through. We have to go past. So that's why I pre-place my VA. If you had for example a four layer board or power on a different layer, for example, 3.3 volts, you would do the same process also for the 3.3 volt VA and nets. And this could also be for signals.

If you know you have to do a jump somewhere, I might pre-place some VAS before I do my routting. You might even have to root out tiny bits of section to see how the signals might flow just to get a feel for where you might need the VA. But in any case, this seems kind of all right for the most part.

One VR I might not be too happy with is I placed one V directly under this tiny accelerometer part. And not my preferred method, but I've done this a couple times with okay results. Ideally, you don't want to really have VAS underneath these small components. But here, it's just so I know lucrative in a way because then we can just route all the ground pads directly into that central via.

We could of course also scatter ground v around here for all these pads. Again, only really pin 9 is a is a proper in quotes ground connection. So, we'll see about that V if we needed later on. I'm just placing it there just to prove planet. Some components for instance sensitive magnetometers or certain components I think uh certain accelerometers as well actually explicitly tell you the data sheet to not put any copper underneath or at least on the same layer underneath these components. For this particular data sheet I didn't see that. So that's why I just put a via here in case with
