# Net Colours



Back to the 2D view, we also saw in the schematic editor that we assigned various colors to the different nets in the PCB. And as we see here, once we've imported the components, we don't really have various different colors. Depending on what layer we're on, that color will be highlighted. So, typically a top copper layer or front copper layer F.

CU CU on the right hand side that will be a red color. If we're routing or routting on the bottom layer then that will be a blue color. So as you can see on the right hand side as I click next to the color box we can see different parts of the PCB get accented or highlighted and that's the current layer we are then working on.

I don't like the default color view and again this is why I do my schematic colors and then transport them over to the PCB because it makes everything far clearer. With everything red or blue here, we can't really tell the difference between powers, grounds, high-speed signals, and so on. So, you might have already noticed, but if you go back to the board setup in the top left of Keycad, then going to net classes under design rules, there's a button which is import colors from schematic.

So rather than having to reassign the colors once in the schematic, then once in the PCB design, we can just import them to whatever we set up in our schematic editor. Once I click that, I go to the right hand side. We can see the PCB colors are now assigned. And we also have a default net class on the PCB design.

Depending on what we're rooting, if we're rooting USB, if we're rooting power signals, we can give these net classes default track widths, via sizes, and so on. So you might want to have a control impedance net class if you're rooting USB or you might want to have wider traces for certain powers. For now, we're going to leave everything as default and just work with the predefined sizes we defined earlier.

But now we have the net close in place. So if I click okay, nothing has changed except you can see the rat's nest which are these essentially air wires which show connections that are still to be made have changed color. I would also like to have the pads and traces and tracks and everything else change color as well.

The way we can do that is go to the right hand side appearance then click on the nets tab in the bottom open the net display options drop down and then change the net colors from just the rat's nest to all. And here we go. This is the kind of view I want. It is quite colorful but this is I find super helpful when I'm rooting.

I can quickly jump to okay where's the USB it's these green patterns where's ground that's everything that's gray where's power that's pretty much everything that's reddish so that's why I find it immensely useful not just for the schematic but also for the PCB design to label my nets and to color my nets the net labels are great as well we know okay this is I squed C1 SDA this is SCCl this is power this is ground this is the reset signal I'd strongly suggest doing this for every single design no matter how small or large the design is with all of this in place we are now ready to lay out the PCB and layout for PCB designs in my opinion is and should be the substantial part of any PCB design.
