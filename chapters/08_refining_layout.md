# Refining Layout



We can see there's some components where the courtyards, you can see this kind of pinkish box hanging off the board and these courtyards shouldn't overlap and they should be away from the board outline as we spoke about before. We tie up this place and then we can start adding in all of these relevant components around the board before we then move over to routing.

We also have these fidial markers and these help the pick and place machines and the automatic optical inspection to find their bearings relative and absolute position. So I take the fiduial marker and I want to place them across the board. So we typically have a minimum of three fedio markers. Typically I will have I'll put one top left, bottom left, and bottom right for instance. But you want them spread as far as you can across the board.

So I might just place one next to the mounting hole like so. Take the second footed marker. Press M. Move it next to the bottom left mounting hole. Take the third marker and move it next to the right mounting hole like so. And clean all this up a tiny bit. If I go to 3D view, this also helps me a lot.

Sometimes you want some overhang on the USB type-C connector, even though there is a tiny bit of distance between the actual shroud of the USB type-C cable or plug that goes into this connector. So, you can actually arrange that the connector edge is flush with the edge of the board. But for now, I'll keep it like so.

We also want to make sure that these mounting holes are sufficiently far again from the board edge. And we here we have about a millimeter. And that's okay. For through hole through holes I like to have a bit further away from the bolt edge than for example SMD components. So a millimeter seems to be around fine. Our ESD protection we typically want a bit closer to our USB type-C connector.

Again leaving space so we can fan out the part, but we want to have it fairly close so we can shunt ESD pulses essentially to ground quickly close to the source. You want our power regulator. We might want to move a bit further away up here so we can fit the supporting circuitry around it. The USB connections you want to keep short as well. So that's why I might want to move U2 a bit closer to D1.

I want to move U3 and its fironic circuitry. So I can drag and hold over it and move it a bit more to the left as well because we do have some supporting components around it. And that also gives me then room to move J2 just a bit further away from the board edge like so. So again, it's an iterative process.

You might want to clean things up just a tiny bit before you start adding in the smaller components. And you'll do this repeatedly for your boards. After having adjusted the layout just a tiny bit as we just saw again as we add in more and more components we might have to move things around. We might have to adjust the pin outs just to make our routting life easier later on. We're now ready to move over adding in the smaller components.
