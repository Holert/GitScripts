# ggplot2 is a plotting framework that is (relatively) easy to use, powerful,
# AND it looks good.

# Jeff Stafford

library(ggplot2)

# Load the example data
data <- msleep
str(data)
# It's sleep data of some kind. Why are we using it? Because I am absolutely
# sick of looking at the gapminder dataset.

####################################################

#Okay, let's start. ggplot2 revolves around a certain kind of variable: the
#ggplot2 object.

# What is a ggplot2 object? Basically it is your data + information on how to
# interpret it + the actual geometry it uses to plot it.

# How to create ggplot2 objects:

# You can add as much data in the inital function call as you want. All of these
# work, but the final version is the only "complete" object that fully specifies
# the data used for the plot. 
ref <- ggplot()
ref <- ggplot(data)
ref <- ggplot(data, aes(x = bodywt, y = sleep_total)) 
# This is the same thing as the line above:
ref <- ggplot(data, aes(x = data$bodywt, y = data$sleep_total))

# To store an object (to add to it later/plot it on demand), just give it a
# reference. Simply typing the reference will display the plot (if you've
# provided enough information to make it.)
ref
# As you can see, we haven't specified everything we need yet.

# IMPORTANT: There are 3 components to making a plot with a ggplot object: your
# data, the aesthetic mappings of your data, and the geometry. If you are
# missing one, you won't get a functional plot.

# Your data should be a dataframe with everything you want to plot. Note that it
# is possible to put data from multiple sources (ie. different dataframes) in 
# the same plot, but it's easier if everything is in the same 2-dimensional
# dataframe.
ref <- ggplot(data)

# The aesthetic mappings tell ggplot2 how to interpret your data. Which values
# in your dataframe are the y-values, x-values, what should be used for colors, etc.
ref <- ggplot(data, aes(x = bodywt, y = sleep_total))

# The geometry is the actual stuff that goes on the plot. You can specify any 
# geometry as long as you have supplied the values it needs. If you've specified
# the required aesthetic mappings (which data corresponds to x, y, etc.), all
# you need to do is tell ggplot2 to create a certain geometry- for instance a
# scatterplot.

# Just add the geometry you want to your object. In this case, we are making a scatterplot.
ref <- ggplot(data, aes(x = bodywt, y = sleep_total)) + geom_point()
ref

# All you need to do to add more information to your plot/change things is add
# on more elements. Lets add a logarithmic scale on the x axis.
ref <- ggplot(data, aes(x = bodywt, y = sleep_total)) + geom_point() + scale_x_log10()
ref

# Lets add a smoothed mean.
ref + geom_smooth()

# You can also specify aesthetics inside the call to create geomtery. 
ref <- ggplot(data) + geom_point(aes(x = bodywt, y = sleep_total)) + scale_x_log10()
ref
ref <- ref + geom_smooth()
ref
# Why didn't that work? This is because when we specfy aesthetics inside a call 
# to geomtery it only applies for that layer (only geom_point got the x and y
# values). The only information that gets passed to all geometery calls is
# aethetics specified in the initial creation of the ggplot object.

# So if we wanted that to work, we'd have to do this:
ggplot(data) + scale_x_log10() + 
  genames(sleepMeans)om_point(aes(x = bodywt, y = sleep_total)) +
  geom_smooth(aes(x = bodywt, y = sleep_total))

# It's important to note that geometry will automatically use any aesthetic
# mappings that it understands, and ignore ones it doesn't. So if you specify as
# much stuff as you can in the inital call that can be used, it'll save you
# work.

# Like this:
ggplot(data, aes(x = bodywt, y = sleep_total)) + scale_x_log10() + geom_point() + geom_smooth()

########################################################
# Let's all try making a plot on our own!

# Make a scatterplot of conservation status vs. time spent awake 

# Hint: conservation status is data$conservation and time awake is data$awake.
# To make a scatterplot, use geom_point().

##########################################################


# Let's follow up with a few very common plot/geometry types and mappings you
# might be interested in:

# These x and y mappings (and the log scale on the x axis will be used for all later plots).
plot <- ggplot(data, aes(x = bodywt, y = sleep_total)) + scale_x_log10()
plot + geom_point()

# First lets add color based on what things eat. Note that it automatically adds a legend.
plot + geom_point(aes(color = vore))

# We used a factor there, but we can also use a continuous variable for color as well.
plot + geom_point(aes(color = brainwt))
plot + geom_point(aes(color = log(brainwt)))

# We can change the legend to change the colors in this case.
plot + geom_point(aes(color = log(brainwt))) + scale_color_gradient2()

# Change the colors
plot + geom_point(aes(color = log(brainwt))) + 
  scale_color_gradient2(low = "green", mid = "yellow", high = "red", 
                        midpoint = -4, na.value = "purple")

# Set the limits of a scale
plot + geom_point()
plot + geom_point() + scale_y_continuous(limits = c(5, 15))


# How about changing size?
plot + geom_point(aes(size = sleep_rem))
# Or alpha (add some titles and labels while we're at it)?
plot + geom_point(aes(alpha = sleep_rem)) + 
  xlab("this is our x axis") + ylab("this is our y axis") + ggtitle("title") + scale_alpha("our legend")

# If we want to simply change a plot value like marker shape or size without
# mapping it to data, just specify it outside the call to aesthetics.
plot + geom_point(aes(shape = vore), size = 6, color = "orange")

# Let's facet our data by a factor:
plot + geom_point() + facet_wrap(~vore)

# Let's put it all together...

library(scales) 
# oob specifies what to do with out of bounds values for any scale (normally the
# value gets changed to NA), "squish" sets them to scale max or min, to use
# squish you need the "scales" package. 

ggplot(data, aes(x = bodywt, y = sleep_total, size = log(brainwt), color = sleep_rem)) +
  scale_x_log10() + xlab("Log body weight") + ylab("Total sleep (hours)") + ggtitle("sweet title") +
  geom_point() +
  facet_wrap(~vore, nrow = 1 , ncol = 5) + 
  scale_color_gradient(low = "firebrick1", na.value = "green", limits = c(0,4), oob = squish)

# Note that we were manipulating aesthetic mappings that geom_point() 
# understands. To see what it understands, check out either the help for 
# ?geom_point or its documentation (with examples) at 
# http://docs.ggplot2.org/current/
?geom_point

################################################################
# Another pop-quiz... 

# How would I make a scatterplot of conservation status (data$conservation) vs 
# time awake (data$awake), with the color mapped to vore (data$vore) and the 
# size mapped to the log of brain weight ( log(data$brainwt) ). Bonus points if you add axis
# labels and a title.

################################################################

# Now for a few other types of plots:

# Boxplot... note that stats are automatically performed, more about that later...
ggplot(data, aes(x = vore, y = sleep_total)) + geom_boxplot()
ggplot(data, aes(x = vore, y = sleep_total, fill = vore)) + geom_boxplot()
# What's the difference between fill and color?
ggplot(data, aes(x = vore, y = sleep_total, color = vore)) + geom_boxplot()

# Line plot with different groups
ggplot(data, aes(x = bodywt, y = brainwt, group = vore, color = vore)) +
  geom_line() + scale_x_log10() + scale_y_log10()

# 1D density
ggplot(data, aes(x = sleep_total, fill = vore)) + geom_density()
ggplot(data, aes(x = sleep_total, fill = vore)) + geom_density(alpha = 0.5)

# 2D density
ggplot(data, aes(x = sleep_total, y = sleep_rem)) + geom_density2d()

# Violin plot
ggplot(data, aes(x = vore, y = sleep_total)) + geom_violin()

# Jittered scatterplot
ggplot(data, aes(x = vore, y = sleep_total)) + geom_jitter()
# Change the width of jittering:
ggplot(data, aes(x = vore, y = sleep_total)) + geom_jitter(position = position_jitter(width = 0.2))

# Jittering a scatterplot + violin plot
ggplot(data, aes(x = vore, y = sleep_total)) + geom_violin() + geom_jitter()
# Notice how plotting order makes a difference here (stuff gets covered up)
ggplot(data, aes(x = vore, y = sleep_total)) + geom_jitter() + geom_violin()

# Bar plot 
ggplot(data, aes(x = vore)) + geom_bar()
# Note that it automatically is binning the number of values in "vore".

####################################################################
# Assignment 3:

# Make a box plot of the amount of sleep (data$sleep_total) per conservation
# status (data$conservation). Fill in the box plot colors by conservation
# status (data$conservation).

# Hint: you will need the following aesthetics: x, y, and fill. The geometry you
# want to use is geom_boxplot()

#####################################################################

# Let revisit the bar plot as an example of how to make things pretty/ the way we want!
ggplot(data, aes(x = vore)) + geom_bar()

data$vore
# Bars are automatically ordered alphabetically (apparently people say that this
# is not a bug, it's a "feature"...). To reorder a factor:
reordered <- factor(data$vore, levels = c("herbi","omni","carni", "insecti", NA))
# Anything that reorders a factor will work to change bar order, order of color labels, etc.
ggplot() + geom_bar(aes(x = reordered))

# Let's graph mean sleep/category instead of just the raw number of animals in 
# each category. This giant block of code will simply calculate the mean of each
# category and the standard error of the mean. I've annotated it if you want to
# follow along.

# Remove NAs
sub <- data[is.na(data$vore) == FALSE, ]
# another way of doing the same thing: sub <- subset(data, is.na(data$vore) == FALSE)
# Get all the unique categories
categories <- unique(sub$vore)
# Preallocate vectors for speed (not necessary, just a "best practices" kind of thing.)
sleepMeans <- rep(NA, length(categories))
# Change the names of our output vector to the names of the unique categories
names(sleepMeans) <- categories
# Create a copy for the standard error of the mean
sleepSEM <- sleepMeans
# Do the actual calculations
for (cat in categories) {
  sleepMeans[cat] <- mean(sub$sleep_total[sub$vore == cat])
  sleepSEM[cat] <- sd(sub$sleep_total)/sqrt(length(sub$sleep_total[sub$vore == cat]))
}
ggplot() + geom_bar(aes(x = sleepMeans, fill = names(sleepMeans)))
# What happened? geom_bar() and (ggplot2 in general) automatically bins values,
# which can be really annoying. So it's counting one value for each level of the factor.

# Use "stat_identity" when calling geom_bar instead (geom_bar() implicitly calls
# "stat_bin") and map a value to y.
ggplot() + geom_bar(aes(x = names(sleepMeans), y = sleepMeans, fill = names(sleepMeans)), stat = "identity")

# Converting to a dataframe for ease-of-use later. Full disclosure: I was having
# trouble with this data as a vector.
sleep <- as.data.frame(sleepMeans)
colnames(sleep) <- c("means")

# Let's add error bars, we calculated standard error of the mean earlier...
plot <- ggplot(sleep, aes(x = rownames(sleep), y = means, fill = rownames(sleep),
                          ymin = means - sleepSEM, ymax = means + sleepSEM)) + 
  geom_bar(stat = "identity")
plot
plot + geom_errorbar()
# Change errorbar width:
plot + geom_errorbar(width = 0.5)


# Let's do an in-depth example (all of this can be applied to other plot types):

# Reorder bars in descending order of their value
idx <- order(sleep$means, decreasing = TRUE)
sleep$name <- factor(rownames(sleep), levels = rownames(sleep)[idx])

# Create a custom color palette with RColorBrewer
library(RColorBrewer)
display.brewer.all()
palette <- brewer.pal(n = length(rownames(sleep))*2, "Spectral")[seq.int(1,8,2)]
names(palette) <- levels(sleep$name)

# Notice that it's just using hexadecimal color codes. You can use a vector of
# any R colors/hex codes you can think of.
palette

example <- ggplot(sleep, aes(x = name, y = means, fill = name,
                  ymin = means - sleepSEM, ymax = means + sleepSEM)) + 
  geom_bar(stat = "identity") + geom_errorbar(width = 0.5) +
  scale_y_continuous(limits = c(0, max(sleep$means)*1.5)) +
  xlab("Food type") + ylab("Average sleep per night (hours)") + 
  scale_fill_manual(values = palette) +
  guides(fill = FALSE) # this kills the redundant legend
example

# Change theme elements to white.
example + theme(panel.background = element_rect(fill = "white"),
                panel.grid.major = element_line(colour = "white"),
                panel.grid.minor = element_line(colour = "white"))
# Or just change a large number of graphical elements at once to a specified theme:
example + theme_bw()

# The ggthemes library has a large number of other themes available. Here's an example:
library(ggthemes)
example + theme_wsj()
# To see what else is available from ggthemes, check out this link:
# https://github.com/jrnold/ggthemes

# To save a file use ggsave(). Defaults to last plot made but you can specify a 
# plot with "plot = plotName" as one of the arguments. File extension is
# automatically chosen based on filename.
ggsave(filename = "example.png", width = 10, height = 10, units = "cm")

# I recommend using the Cairo package when exporting, as it performs
# antialiasing. This will only make a visible difference in plots with lots of
# tiny datapoints or complex shapes (ie. not a bar plot).
library(Cairo)
ggsave(filename = "example-cairo.png", width = 10, height = 10, units = "cm", type = "cairo-png")

# So yeah, ggplot2 is a pretty powerful (but tricky) package. To see what's possible, read
# the documentation at: http://docs.ggplot2.org/current/

# Also helpful: 
# http://zevross.com/blog/2014/08/04/beautiful-plotting-in-r-a-ggplot2-cheatsheet-3/

# Here's a few frustrating errors I've run into from time to time (note that I'm
# paraphrasing here... it might not match the exact text...)

# Error: ggplot does not know how to interpret class numeric (or matrix, etc.)
# Solution: Make ALL of your data into dataframes. ggplot2 hates everything else.

# Error: Aesthetics must be length one or the same length as the data. 
# Solution: Make sure all of the aesthetic mappings your are feeding to ggplot2 
# are the same length. If it seems like they are, you might be passing the wrong
# aethetics to different geometries (especially if they use different data).
# Sometimes an aesthetic from the initial function call gets passed along when
# it shouldn't and you need to set it to NA.

# Error: No layers in plot.
# Solution: Add some geometry.



