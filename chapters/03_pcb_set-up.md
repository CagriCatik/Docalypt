# PCB Set-Up



After uploading, of course, I detect a small little correction we need to make, and that is the USB D minus and D plus lines are connected correctly, but of course, the net labels, you probably noticed in the previous video, need to be flipped at the USB UA converter. So, USBD minus needs to be moved to USBD plus and vice versa. So, I'm going to click on that, Crl X, Ctrl +V, just paste that somewhere else. And I'm just going to move these two around. There we go.

And now, actually, the net labels match up with how everything is routed as well. But other than that, we are now ready to move over the PCB design. Remember last time we also had assigned the footprints and we've done the electrical rules check. So unless you spot something else, the schematic in my eyes looks pretty okay for now.

So to move over to the PCB design, we go to the top toolbar. You can see the far right button is switch to PCB editor. If I click on that, a new window will open. This is going to be our view for the next remaining part of this video, at least for a large part of it. We have our main PCB editor, and the controls for moving around are fairly similar to the schematic as well.

We can hold the middle mouse button and then move around to drag the PCB design, zoom out with a middle mouse wheel, zoom in with the middle mouse wheel. We also have a rather than just this 2D view, we have a 3D view. If you go to the top left, view 3D viewer. We can also press Alt + 3 as indicated by this shortcut info here. And so far we have a pretty undefined, pretty poorly defined PCB.

That's why you're not seeing any shape or anything. And we can see the board outline is missing, but we'll get to that later on once we've added some components onto this. On the right hand side we have our layer view. So we have a front copper, back copper, various paste layers, silk screen and so on. And we won't be using all of these. We only need a certain subset of these specifically also just for a two-layer board.

Tool bars on the right, tool bars on the top as usual, but we'll go through this as we need when we progress through this design. The first thing before we import any components, what I do is set up my PCB design and my board. The way we can do that is go to the top left and click on board setup. We'll go through this board setup bit by bit.

We might not go through all of it, but I find it's important to set up your PCB, your PCB design constraints. For instance, how narrow you can make your traces, how nar how small you can make your drill holes and so on. I strongly suggest you do that before you start laying out routing or anything else. You want to make sure your design is manufacturable.

And by going through the board setup initially, you can ensure that you don't have to change anything later on once you notice, oh, actually it isn't manufacturable. So, we want to stay within certain constraints. But first of all, the board stack up looking at the board editor layers. They're only certain layers we need for us. I will not be using the fabrication layers. We don't need adhesive layers.

This is not part of this specific PCB design. So I can click on these little check boxes to remove those layers just to give ourselves a far clearer view of the PCB as well as the PCB layers. Paste is important. That's our solder paste. Silk screen at the front. Solder mask is important. Of course, our copper and our front copper back copper.

And you can for copper layers on the right hand side change what type of copper layer it is. So if it's a signal to power plane mix for us we're really going to estimate that our front layer or our top copper layer is going to be predominantly signal and power routting and our bottom copper layer we want to keep as much as we can a solid ground plane.

So that's why the bottom copper layer I'm just going to change to power plane. Now there actually isn't very much of a significance here other than just for completeness sake but it doesn't actually change terribly much. Turning off all of these other layers just to make this clean. These are the sets I want. I just want copper. I want paste, silk screen, and mask layers as a bare minimum.

Then the physical stack up going on the left hand side. We can change how many layers you want. Keycadly supports up to 32 layers. Impedance control as well. And this is just information for you and also later for your manufacturer to tell them how you want your PCB stack up. So what materials you want to use, what thicknesses, what copper files and so on.

A lot of this you can keep as standard. So for the two-layer board, we can see the overall board thickness. If we look at the bottom, Keycad has calculated this as 1.6 mm nominal. And that's typically what a two-layer board thickness will be at. So for us, we can just keep this as as this is board finish. We can change what type of copper finish we want.

Again, this is just for completeness completeness sake. And when you create manufacturing drawings and assembly drawings, this can be very helpful to tell the manufacturer exactly what you want. For us, we'll just go with a hot air surface leveling lead free finish for now. This is a fairly simple board. Would have had very fine pitch components.

So, let's just go with hot air service living lead free. This isn't terribly important if you don't set this up for now. Solder masking paste is the first actual parameter we really need to change. Solder mask expansion. We can go to the JLC PCB site to see some some examples of this.

Typically, your top and bottom layers will be covered with solder masks except where the areas are where we have exposed pads. So that's why we don't want want any solder mask because of course you want to solder components to those areas and to those pads. So therefore the solder mask is actually a negative or rather an inverted layer. Anytime you see something on the solder mask layer that's where there is no solder mask.

You don't just want to have the solder mask opening exactly fit the shape of the pad with essentially zero solder mask expansion. You want it slightly larger cuz there are misregistrations, misalignment issues with solder mask. Of course you can't have a perfect 100% accuracy of alignment of your solder masks. So that's why we have this solder mask opening.

Still a very small amount and that depends on what your manufacturer is capable of doing. If we'd go to the JLC PCB manufacturing assembly capabilities section and every PCB manufacturer will have this on their website or you can ask them to send this to you. Scrolling down to the solder mask section.

We can see the solder mass expansion capability can be actually 1:1 which is pretty good. But typically I like to keep this at for simple design something like 0.1 mm or slightly below that. We also have some other parameters we have to stay within. For example, minimum solder mass bridges or slivers. So, how narrow the webs can be. And you take all of that from your assembly and manufacture house.

Then going back to keycode, I'm just going to type in 0.1 mm for my expansion, 0.1 mm for my minimum web width, and 0.1 mm solder mask to copper clearance. Solder paste settings we can just leave as default. Text and graphics, you can change your default line thicknesses, widths, and so on, but we'll get to that a bit later as well.

What we want to jump straight to is the design rules and the design constraints. This is incredibly important to set up again because we want our PCB design to be manufacturable. We don't want to have minimum clearance of 0 mm. That's impossible. Minimum track width of 0 mm. You really, really have to set this up. And again, you set this up by going to your manufacturer, checking for instance traces, what they can do.

They can do for two layer boards minimum track width and spacing of 0.1 mm. And that's very very very narrow and very thin traces. That's what they could theoretically do for 1 oz copper on one or two layer boards. However, you always want to stay away from manufacturing minimums.

The more strict you make your design rules, that is you go further away from the manufacturing minima, the easier your design will be to manufacture. And that's what you want. You want a higher yield. you want most of your PCBs making it through the manufacturing process without having to be scrapped because there will of course be manufacturing deviations and tolerances. So that's why we try to stay away from these minimums.

I have because I've done this quite a number of years and I've done many many PCBs. I just have certain minimums I have in mind. If I go for a two-layer board, for a simple four layer, for an advanced four layer or multi-layer boards, this kind of comes with experience the values we'll be entering here.

But they're also based on minimums that your manufacturers and also really affordable manufacturers can do. Minimum clearance I'm going to do 0.152. And these weird.152 numbers or 0.254 come from mills and millimeters these conversions. So again we talked about in the schematic section that we try to keep things with mills.

So 100 mil grid but when we come to the PCB we typically use millimeters or at least in Europe we do. So therefore you could type in 0.15 but.152 translates to 6 mil and that's about 0.152. That's why I take that number and that's still a very very small number. Same for track width.152 and we'll try and keep away from this. This is just the absolute minimum when we do our design rule check later on.

Connection width same minimum annular ring. If we look at drills our annular ring is essentially the copper that's left over after drilling through the pad. So the outer diameter minus the inner diameter divided by two. However, when you're drilling a hole, manufacturers typically drill plus or.

1 mm larger and then plate down to the final drill size. Minimum annular rings, therefore I like to keep at at least 0.15. Minimum V diameter I will go with 6. Copper to hole clearance I like to keep at.254 and copper to edge clearance. So essentially to the board clearance.5 is a good value. You can go down to 04 for V-cut and 3 for cutting typically but.

5 again staying away from manufacturing minimums. Minimum through hole.3 whole hole clearance 2554. We'll not be using will not be using microv. Minimum text height 8 is kind of pushing it. That's okay. Minimum text thickness I'm going to go with 0.1. Predefined sizes. This is the way Keycad works.

We can predefine track sizes, via sizes, and then scroll through them when we go to the PCB design. Rather than entering specific values every time we route a trace, we can just enter predefined track widths. And I have my set of track widths that I like to use. For instance, I like using.3 mm traces for two-layer boards if they're signal traces and anywhere for instance.5 and 1 mm traces for power.

For VAS, my standard via is a 7 mm diameter with a.3 mm hole. We do also have differential pairs because of our USB D minus and D plus nets. So we should fill in that information as well. Now typically for USB 2.0 we want a controlled impedance differential pair. But we're using USB 2.0 full speed.

So essentially as slow or as quick as SPI we're using very we're going to have very short traces. So actually the control impedance doesn't really matter. And the actual way we root our differential pairs for this design really does not matter. However, we should enter a value because Keycad assumes it wants to root a differential pair and we need to provide it with some information.

Trace width might be.3. A gap might be.3 as well and a V gap of let's say.5. I'm just guessing these values just for now. We can adjust them when we come to the USB differential pair later on. But again, these are some typical trace values you might use.3 for a good signal trace. And again, not controlled impedance. Power trace is larger. my standard via.

You can lose larger VA, but I'd strongly suggest not going with smaller VA unless you have a good reason to. And differential pairs, just a value to get started, but we'll adjust this later on. Teardrops we'll look into later when we clean up the design. We have net classes, and here these were taken over from the schematic. So, we have our crystal, we have Vray, 5 squed C, and so on.

And for these different net classes again why I like to do them also like to define them in the schematic is because they one carry over to the PCB design but we can segment the way we route into different classes. So for instance we might want to route power and ground structures different to our sensitive crystal structures or for example to USB.

You could of course just stick with the default net classes but it depends on certain scenarios. You might want to have increased clearance or greater track widths, greater via sizes and so on. You can set custom rules as well. You can set violation severities for the design rule check. But for now, this is the bare minimum setup I would do for typical PCB design. Click okay to save.

Now that we set up the PCB design, we can see on the right hand side the layer count has shrunk significantly. Again, this is still a two-layer board, but we don't just have copper layers, we have other layers as well. With the PCB now set up, let's go to the top toolbar. You can either press F8 or click this little button, update PCB from schematic.
