# Layer Assignment & Polygon Pours



It depends on the type of components. If you're using just standard through VAS or if you're using blind buried VAS, microv, that'll all influence how we route things. But this board is incredibly simple. It's going to be a simple two-layer board. Our front layer, front copper layer, just has all of our components on it.

And we'll be using this predominantly for signal and power routting. The bottom layer, where there are no components, we will do a single large polygon pole that spans the entire area of this board. This will provide a fairly nice low impedance ground reference that we can connect all of our ground pads to with shortwire connections and VA that we can then just drop down to that layer.

And that's a pretty standard practice to have your primary layer single power and your bottom layer ground for a two-layer board. And this is going to be pretty much sufficient for this type of board. The way we can create a polygon pole is on the right hand side draw zones. And you might want to increase your grid size by pressing shift N or just selecting the toolbar.

So I'm just going to 1 mm grid. Click on draw field zones or control shift zed. And I'm not going to bother with following the contour because keycad will automatically fit the polygon paw to the actual outline. I just leftclicked and now you get this copper zone properties. I want this for now just on the bottom copper layer. And our net I want to be ground.

So I can just type in G and ground. Zone name. I like giving my zones names cuz they're easier then to find. So I'm just going to call it layer two ground. My second layer or my bottom layer ground. You can change various parameters here such as the solids or hatch fill if you want to remove islands and that's pretty much always the case as well as electrical clearance. Now this is a very very generic electrical clearance.

This is a clearance to anything. This is a clearance to holes. This is a clearance to outline. This is clearance to traces which isn't terribly great because there are different design rules for different copper to feature clearances. A fairly reasonable number is 0.3 mm. That's a kind of catch all case and that's pretty much produced by about any manufacturer.

Keep in mind this will also be the board auto polygon pore clearance. So let's increase that a bit to 04. Minimum width that's the minimum copper feet width which also should relate to your trace width minimum. And for PCBs that's for two-layer PCBs you can go down to something like 2 or even 0.15.

Pad connections for a large solid ground plane or any polygon pore we have to worry about thermal imbalances. one for small components and also two that for instance if you solder a through hole pin to a large copper mass it's going to take a very very long time you have to heat up the board and that's why we might want thermal relieves pad connections and that's what you can define here size of them IPC has some various standards and suggestions of how to do that but typical values might be 3.3 for the relief gap and the and the spoke width and these are just fairly

generic numbers for now corner smoothing I would like to implement as a as a fillet and now I can click Okay. And we can start actually drawing the outline. So, we clicked on the bottom left. I'm going up and I'm just going to follow this outline. And you can see this polygon shaded area start to appear. Click on the initial starting point. And that closes the polygon.

Escape to cancel. And now nothing's really poured. I can press B on my keyboard and that repor the polygon on the bottom layer. If I go to the right hand side, right click and hide all layers and then just enable the bottom copper layer, we can see we have a large holog that fits the outline with a certain clearances we specified.

And we see we have thermal relieves on, for instance, the USB mounting hole, the shield connections, which is what we specified. But also, we have thermal relieves on our mounting holes. And we're not really going to solder anything to the mounting holes. These are mounting holes for screws. So that's why that doesn't really make sense to have thermal relieves on these. But that's the default property of these footprints.

So I can hover over one of these, press E, and then go to the connections tab on the pad properties. And here we can see connection to copper zones. And currently the pad connection is from parent footprint. And we don't want that. The key to put footprint has thermal reliefs. We want this to be solid. Click okay. Press B again to repour.

And now we have a solid connection to our mounting holes, which makes sense. And we want to do that for the remaining three as well. And that's exactly what we've done. And here we go. We've got a polygon pole on the bottom layer. And that's going to be our predominant ground connection. So anytime we want to connect ground, we go to the top layer, route out a bit, drop a via, so Zaxis connection, and that then links up to the bottom layer to our ground plane. In 3D view, we can see on the top layer, we don't have anything other than components. But on the bottom

layer, now we now have this polygon pore with the relevant clearances to all of the features because of this rather generic electrical clearance rule. with our polygon paw on the bottom layer in place which is connected to the ground net or assigned to the ground net.
