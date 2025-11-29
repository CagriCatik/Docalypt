# Power Layout



But again, in terms of order of criticality, R2, R3 aren't as critical, for instance, as the power path. Again, of course, they're needed, but in terms of placement, we could place R2, R3, as a joke, on the moon, and it would probably still be okay. But, but our our power line is more critical than R2, R3, for instance. So, we might want to do our power rails first before we then put on R2, R3.

So, let's just start, for instance, with C1, which is our input capacitor from the USB connector. And the USB connector of course has two orientations rotated 180 degrees. So we always have the double double sets of pins. We have double sets of D minus D plus CC pins VUS and ground.

So we could place C1 down here next to V bus and ground. But actually we've placed our U1 regulator at the top. So it makes sense to place it on the opposite side because our power path is going to be from the USB connector through a Pi network into U1 and out of U1 for 3.3 volts.

I would suggest placing C1, R1, C2, our pi filter up here somewhere. So that's why we would take an R1 which is our our placeholder series element and I'm going to make it align with D1. This C1 R1 C2 isn't any bypass decoupling. It's simply a filtering network which is a placeholder. It should be close to your power source of course but and it shouldn't be too far away but it doesn't have to be as close as for instance you know our bypass and decoupling capacitors.

So something like this might be okay. And then symmetrically we can take C2 and put it on the other side. For instance, that would look something like this. So that's one method of doing a PI filter. What I prefer, which is a slightly bit more compact version, is actually this structure. To me, in this scenario, this is of course just a tiny bit more compact.

We have to keep sure now not that it makes terribly much of a difference that we route from the V-bus power into the C1 capacitor pad first then into R1 out of R1 into C2 and then only into U1 through the capacitors as well rather than going from USBC jack USBC connector into R1 then C1 and so on but it's a minor difference. We'll come to that when we get to the routing later on.

So again closeish to Vbus not too far away and not too close that become we have difficulties with soldering and assembly. You could also line this whole structure up like so say that R1 is aligned with C7 for instance might make it a tiny bit neater. So something like that might be a good starting point.

This also keeps the Vbus connections then short between Vbus of the R1 network as well as Vbus of the ESD the TF TVS diodes on the USB line. So we want to keep that connection short. So this this is why this placement might be favored as well although the components are quite close. In case now we've done our PI filter, C1, R1, R2. Let's move over to the audio regulator.

Now, all of these components are of course important, but the most important components are C3 and C5. C4 is an optional bypass capacitor, which which can help to reduce the output noise on the 3.3 rail, which in our case isn't that terribly critical. So, let's start off with C3 and then C5 and then place C4. Taking C3, this is a larger 0805 capacitor.

Again, now we have the issue of is pin one the power pin or pin 3 the power pin. They both have the same net label. Looking back, pin one is the power input, and that's where our input capacitor should be. Pin three is simply just an enable input pin. A high impedance input pin. So, we have to rotate our capacitor by 180°. Place it close to U1.

Move the silk screen out of the way. Like so, might be a good starting point. We also have to think about where we're going to place VAS, our ground connections later on. So, we might want to keep a bit more space to be able to fit a via in. But, as an initial guess, this seems to be okay. Now we need the output capacitor and that's fairly unambiguous. It's C5 placed close to the output.

So we have this kind of symmetrical layout. Input capacitor LDO output capacitor. You could of course place the out capacitor also like so. And this could work as well. Of course, you're still giving a very short connection between pin one and pin 5. And your ground loop, your overall current loop is also quite small.

But in this case, this layout is in my eyes preferred because it's more symmetrical. And our power ground loops are very similar between those two scenarios as well. Lastly, then we have C4, which is our optional filtering capacitor. And depends on what regulator you choose, you probably won't have this. I'm just going to place this somewhat symmetrically close to the device.

You want to keep the connection between pin 4 and pin one short and reasonable. Not too close, not too far away. Again, always checking in 3D view if it looks reasonable to you as well. So, something like this might be an okay starting point for layout. We have plenty of board space to move things around. If we feel like things are getting too tight with rooting, we need to give a bit more space.

We can relax our initial layout a bit more as well. But you saw as we progress through the schematic, we did things fairly logically based on criticality and then section by section and then stitching those sections together. We of course still have the pull down resistors on the CC lines pin R2 and R3.

And these need to be placed somewhat sensibly as well. So we have CC1 and CC2. Now CC2 is easier to access which is R2. We could place it for instance somewhere like so. Keep in mind we still have to route out Vbus and ground and all of that. And ideally we would want to just place C1 symmetrically at the top maybe like so.

But now CC1 CC1 interferes with Vbus and that's what we just spent a bit of time on getting the PI filter somewhat right. So that might not be great to have there and probably isn't great to have there. If we go to 3D view, some USB connectors have their shell resting directly on the board.

Now, of course, it's kind of eyeballing it with this USB connector, but the shell here is actually lifted off and doesn't make direct contact with the solder mask or the top layer of the printed circuit board. I bring this up because often times you will not want to, for instance, root underneath the USB connector because you shouldn't be seeing in the solder mask, that is that top surface covering which protects the copper layer underneath. You shouldn't be seeing that as an insulator.

While it is an insulator, it's not a particularly great one and solder mask can fail and I wouldn't rely on it as an insulator. For our case, for sake of simplicity and also because this actual USB connector, the shell is raised off away from the solder mask. I think it's okay to route underneath in this particular case.

So, what we could do is just place R2 and R3 somewhat symmetrically. And that means we can then simply route underneath. So, out of pin B5 underneath the USB type-C connector into CC2 and similarly and symmetrically for USB CC1, pin A5 into R3. And that just makes our lives easier because now it doesn't block VBUS. At least outside doesn't block VBUS.

We'll see. We'll have to do a jump for VBUS anyway. But this makes it maybe a tiny bit nicer and cleaner. With that being said, this might look like an initial layout. Okay, there might still be things to clean up. We have silk screen, which is superolous.

For example, for the mounting holes for the fidial markers, there's some silk screen hanging off the board which you need to clean up. But the main point I'm trying to illustrate is that we should spend a fair amount of time doing a proper layout. It'll make our lives a lot easier when it comes to routing later on. We've really thought ahead of what connections need to go where. We've really done some pin mapping, pin swapping based on what we think our routing is going to be like.

We've placed components as we think would be optimal, also considering power, decoupling, bypassing, signal length, and so on. And all of that without doing a single route. It's all just essentially visually doing the layout. Again, all components on the top side, no components on the bottom side.

A fairly arbitrary shaped board outline just to make our lives a bit easier, make this board fairly simple. We can add some graphics later on and various information that is typically necessary on a printed circuit board. For now, the last steps I would like to do, clean up the mounting holes.

So, I'm going to click double click on the reference properties and or the silk screen and uncheck visible. do that for the fidutial markers as well. I can also click and press E. It's the same thing. And of course, you can clean up the rotations of the silk screen with placements on. I wouldn't spend too much time on that.

I usually do this kind of clean up right at the end of the PCB before I'm about to produce manufacturing files because there is a high chance that our placement layouts will change. Things will interfere. So, don't worry too much about silk screen, but do keep it out of the way so it doesn't interfere with you being able to see net names, pads, and so on. For now, this seems like a fairly sensible attempt at an initial layout, which means we can move over to rooting very shortly.

With this hopefully somewhat sensible layout in place for this rather simple board, we can move over to rooting. And there's a couple things I would like to talk about before we begin routting. That's first of all, of course, the stackup of the board. That's something you can decide beforehand and you might adjust during your routting process. Depends on the amount of components.
