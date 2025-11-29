# Routing SWD



for example, our debug connections or our UARD connections and so on and fan those out and route those out to the relevant peripherals. What springs out immediately is we can just go on the right hand side. So we can do the serial wire clock serio and for that I'm just going to insert my 0.3 m trace width to start with clock. We can start on the pad.

Press X go out and as soon as I'm out of the pad I don't want to go straight to the right because my serial wire debug connection will be below it as well. I want to come out of the pad and then immediately give myself space. So come out, go up to the top, past here, and then I need to fit through. And because this is a 0.

3 mm trace and as I try to come through here, you can see key cut is not letting me of course because of the design rules. And this is exactly why you set up design rules before you start any routting. Cuz if we didn't, we would have basically unmanufactured board. But this is no issue because we can simply place a track as far as we'll go. Click. And then I'm going to change my my routing width to something a bit smaller to get through that gap.

Escape that gap and then change back to my larger width by pressing W. So something like this might be in order. We come out of the pad with our standard trace width 0.3 mm. As we have to only we neck down in the areas where we need to. Once we've escaped those neck down areas, we try to increase our trace width again because this just improves manufacturability.

We will then do the same thing for serial DIO. So, we'll go back to 0.3 mm trace width. Press X on the pad. We don't want to hug the serial clock pad, but we can already escape a tiny bit below because we're aiming for pad 2 of the tag connect header.

We go in, we neck down a bit by pressing shift W, go through, and then we neck up again and go back to 0.3 mm. For example, something like this. Not maybe the entirely the prettiest, but of course, you can fine-tune this a bit later. For example, we can just use Keycad's drag mode. I'm just clicking and dragging with my left mouse button to just move the tracks and make them a tiny bit nicer.

But of course, you can fine-tune as much as you want. But that's the general idea. We also have the end reset signal. And this end reset signal looks like it just needs to travel underneath the mic controller. And that's typically pretty fine, pretty okay to do that. If you have other options, if you go around, then that's probably better as well. But if we went around, we have a pretty long path to get there.

So for us now, we're just going to go under the mic controller. There's no other signal, at least for now. Of course, we still have to come to power routting later on. That has to go underneath. So now we can just route the end reset signal again with a 0.3 mm trace width. We just go between those pads. We escape. I could go straight into pad two here, but that for me is a bit close hugging pad 25.

So that's why I'm just going to go out a bit, up a bit into pad two, into pad one of the capacitor, and then out of the capacitor again these 90° sections. And then we do the usual necking down procedure as before. For instance, something like this might be okay.

Not the prettiest again, but this is just a simple demonstration. We have the I squed C connections and we have then the UR. So why don't we do the I squed C connections first and as well as the interrupt connections because then we can start moving, you know, from right to the left hand side and finishing up with USB and then doing the power. So it's the same procedure as before.
