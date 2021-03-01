"""
General functions useful for plotting with python-ternary and
matplotlib.
"""

import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.transforms import blended_transform_factory
from matplotlib.ticker import NullFormatter
import ternary


def isiter(x, string=True):
    """
    Little function that checks if a value is iterable. If
    *string=False*, strings don't return true values.
    """
    try:
        iterator = iter(x)
    except TypeError:
        return False
    else:
        if string or not isinstance(x, str):
            return True
        else:
            return False


def cut_dataframe(df, column, divisions, include_ends=True, append=""):
    """
    Return a dictionary of dataframes, cut from *df* along values of
    df[*column*] provided in *divisions*, an array of numbers.
    *include_ends* indicates whether values greater than highest or
    lower than lowest value in *divisions* will be included, and can be
    either None, False, 'low', 'high', or 'both'/True.
    """
    divisions = sorted(list(divisions))

    datadict = {}
    if include_ends in ("low", "both", True):
        label = f"<{min(divisions)}{append}"
        datadict[label] = df[df[column] < min(divisions)]
    for i in range(len(divisions) - 1):
        label = f"{divisions[i]}–{divisions[i+1]}{append}"
        datadict[label] = df[
            (df[column] >= divisions[i]) & (df[column] < divisions[i + 1])
        ]
    if include_ends in ("high", "both", True):
        label = f">{max(divisions)}{append}"
        datadict[label] = df[df[column] > max(divisions)]

    return datadict


def midlegend(ax, loc="upper center", bbox_to_anchor=(0.5, 1), frameon=False, **kwargs):
    """
    Helper to paint a matplotlib legend in the middle of two
    side-by-side axes in a two-column figure setup. *ax* is
    either of the axes, keyword arguments are passed to
    pyplot.legend.
    """
    trans = blended_transform_factory(ax.get_figure().transFigure, ax.transAxes)

    return ax.legend(
        bbox_transform=trans,
        bbox_to_anchor=bbox_to_anchor,
        loc=loc,
        frameon=frameon,
        **kwargs,
    )


def ternary_normalize(data, *cols, suffix="_cnm"):
    """
    Add three columns that are normalized to each other's relative
    precent. *suffix* is appended to the end of the columns.
    """
    assert len(cols) == 3, "ternary_normalize() should normalize over 3 columns"

    for col in cols:
        data[f"{col}{suffix}"] = data[col] * 100 / data[list(cols)].sum(axis=1)


def format_tern_ax(
    ax=None,
    labels=None,
    labelsides=False,
    title=None,
    ticks=False,
    grid=True,
    removespines=True,
    scale=100,
    fontsize="x-large",
    ticks_kws={"axis": "lbr", "linewidth": 1, "multiple": 10},
    bound_kws={"linewidth": 1, "zorder": 0.6},
    grid_kws={"multiple": 10, "color": "grey", "linewidth": 1, "zorder": 0.5},
):
    """
    Wrapper to return a ternary ax with optional grid, title, labels.
    *ax* is either None (creates a new fig and axes) or a matplotlib
    axes object.
    
    *labels* is a three-element array of strings in the order left, top,
    right for labelling ternary plot tips, or if *labelsides=True*,
    ternary plot sides. *scale* is an integer of subdivisions for
    ternary axes; *fontsize* controls the size of label and title text.
    
    *ticks_kws* is a dictionary of parameters for tax.ticks(),
    *bound_kws* for tax.boundary(), *grid_kws* for tax.gridlines().
    
    *labels*, *title*, *ticks*, *grid* can be set to False/None to turn
    off each respective item. *removespines* removes the regular
    matplotlib spines from the axes.
    """
    # Initiate ternary plot
    if ax:
        tax = ternary.TernaryAxesSubplot(ax=ax, scale=scale)
    else:
        fig, tax = ternary.figure(scale=scale)

    # Draw Boundary and Gridlines
    tax.boundary(**bound_kws)
    if grid:
        tax.gridlines(**grid_kws)

    # Set Axis labels and Title
    if title:
        tax.set_title(title, fontsize=fontsize)
    if labels:
        if labelsides:
            tax.left_axis_label(labels[0], fontsize=fontsize)
            tax.top_axis_label(labels[1], fontsize=fontsize)
            tax.right_axis_label(labels[2], fontsize=fontsize)
        else:
            tax.left_corner_label(labels[0], fontsize=fontsize)
            # offset makes it look more symmetric
            tax.top_corner_label(labels[1], fontsize=fontsize, offset=0.18)
            tax.right_corner_label(labels[2], fontsize=fontsize)

    # Set ticks
    if ticks:
        ternary_ax.ticks(**ticks_kws)

    # Remove default Matplotlib Axes
    if removespines:
        tax.get_axes().axis("off")

    return tax


def draw_ternfig(
    nrows=1,
    ncols=1,
    midax=None,
    labels=None,
    figsize=(10, 10),
    spacing=(0.5, None),
    **kwargs,
):
    """
    Return a figure and a list of standard ternary axes on it.
    *nrows*, *ncols* define number and arrangement of axes returned.
    *midax* can either be None, *top* or *bottom*, and will make the
    respective row have one centered axes. *spacing* is a tuple of 2
    floats to be passed as wspace and hspace to
    matplotlib.gridspec.GridSpec.
    
    *labels* is either None, a 3-element tuple of labels that will be
    applied to all axes, or an iterable of such tuples, one for each
    ternary axes. Special values are 'cn', 'cnm', 'cn-k*', and 'cnm-k*'
    (can also be passed in an iterable) that will produce a CN(M)-A-K(*)
    plot.
    
    *kwargs* are passed to format_tern_ax().
    """
    if midax:
        numaxes = nrows * ncols - 1
    else:
        numaxes = nrows * ncols

    # Generate labels
    if labels:
        special_values = {
            "cn": ("CN", "A", "K"),
            "cnm": ("CNM", "A", "K"),
            "cn-k*": ("CN", "A", "K*"),
            "cnm-k*": ("CNM", "A", "K*"),
        }
        if isinstance(labels, list) or any([isinstance(l, list) for l in labels]):
            raise TypeError(
                "*labels* must be either a special string, a 3-element tuple, or a"
                + "tuple of special strings and/or 3-element tuples."
            )
        if labels in special_values:
            labeliter = [special_values[labels] for i in range(numaxes)]
        # 3 non special strings that are not iterables will be applied
        # to all axes.
        # `set1 & set2` returns a set with any shared values
        elif (
            len(labels) == 3
            and not (set(labels) & set(special_values))
            and not any([isiter(l, string=False) for l in labels])
        ):
            labeliter = [labels for i in range(numaxes)]
        # otherwise, iterate over all, determine if special keyword
        # case-by-case
        else:
            assert (
                len(labels) == numaxes
            ), "Number of label arrays or keywords provided \
must equal number of axes requested."
            labeliter = []
            for l in labels:
                if l in special_values:
                    labeliter.append(special_values[l])
                elif isiter(l, string=False) and len(l) == 3:
                    labeliter.append(l)
                else:
                    raise TypeError(
                        "*labels* must be either a special string, a 3-element tuple,"
                        + "or a tuple of special strings and/or 3-element tuples."
                    )

    # Generate figure frame
    fig = plt.figure(figsize=figsize)
    gs = GridSpec(nrows, ncols * 2, wspace=spacing[0], hspace=spacing[1])
    # handle a central ax
    if midax == "top":
        fig.add_subplot(gs[0, ncols - 1 : ncols + 1])
        for row, col in itertools.product(range(1, nrows), range(ncols)):
            fig.add_subplot(gs[row, col * 2 : col * 2 + 2])
    elif midax == "bottom":
        fig.add_subplot(gs[-1, ncols - 1 : ncols + 1])
        for row, col in itertools.product(range(nrows - 1), range(ncols)):
            fig.add_subplot(gs[row, col * 2 : col * 2 + 2])
    elif midax:
        raise ValueError("'midax' can only be None, 'top', or 'bottom'.")
    else:
        for row, col in itertools.product(range(nrows), range(ncols)):
            fig.add_subplot(gs[row, col * 2 : col * 2 + 2])

    # fill figure with ternary axes
    taxes = []
    if labels:
        for ax, l in zip(fig.axes, labeliter):
            taxes.append(format_tern_ax(ax, labels=l, **kwargs))
    else:
        for ax in fig.axes:
            taxes.append(format_tern_ax(ax, **kwargs))

    return fig, taxes


def scatter_tern_color(
    tax,
    df,
    right,
    top,
    left,
    colorcol=None,
    divisions=range(0, 101, 10),
    include_ends=True,
    bring_forward=None,
    colors=None,
    symbols=None,
    **kwargs,
):
    """
    Scatter normalized data on *tax* ternary axes. *right*, *top*,
    *left* and *colorcol* are column names in the *df* DataFrame.
    Data are subdivided and colored separately based on *colorcol*,
    if it is None, all data are scattered in the same color.
    
    For a numerical *colorcol*, *divisions* is an array of numbers by
    which to subdivide the data to be plotted. *include_ends* decides if
    values lower and/or higher than the outer values in *divisions* are
    included and can be either False, 'low', 'high', or 'both'/True.
    
    *colors* is either a single matplotlib color name to be used for
    all data points, an array of color names equal in length to the data
    subdivisions, or a name/object corresponding to a matplotlib
    colormap. *symbols* can be either a single matplotlib symbol name,
    or an array of symbol names equal in length to the data
    subdivisions. *bring_forward* is either a string or list of labels
    in *colorcol* whereupon the scatter object will be set to a zorder
    of 1.5, so as to bring it forward.
    
    *kwargs* are passed to ternary.scatter.
    """
    tern_columns = [right, top, left]

    if colorcol:
        # get the total number of sections
        if str(df[colorcol].dtype) in ["object", "categorical"]:
            num_sections = len(df[colorcol].unique())
        else:
            num_sections = len(divisions)
            if include_ends in (True, "both"):
                num_sections += 1
            elif include_ends in ("low", "high"):
                pass
            elif not include_ends:
                num_sections -= 1
            else:
                raise ValueError(
                    "*includeends* must be either False, True, "
                    + "'low', 'high', or 'both'."
                )

        # parse *colors* and generate list of colors
        if colors == None:
            colorlst = [colors for i in range(num_sections)]
        elif colors:
            try:
                # a colormap, divided equally
                colormap = plt.get_cmap(colors)
                colorlst = [colormap(x) for x in np.linspace(0, 1, num=num_sections)]
            except ValueError:
                # a single color name or no colors provided (left to default)
                if isinstance(colors, str):
                    colorlst = [colors for i in range(num_sections)]
                # list of colors
                elif isiter(colors, string=False) and len(colors) == num_sections:
                    colorlst = colors
                else:
                    raise ValueError(
                        "*colors* needs to be a color name, a colormap name, or an "
                        + "array of color names equal in length to the data divisions "
                        + "to be plotted."
                    )

        # subdivide the dataframe
        if str(df[colorcol].dtype) in ["object", "categorical"]:
            datadict = {v: df[df[colorcol] == v] for v in df[colorcol].unique()}
        else:
            datadict = cut_dataframe(
                df, column=colorcol, divisions=divisions, include_ends=include_ends
            )

        # plot data on the axes
        for (label, data), color in zip(datadict.items(), colorlst):
            if data.shape[0] >= 1:  # check to not plot empty dataframe
                if colors:
                    # need to make colors into a 2D-array to satisfy matplotlib
                    color = [color for val in data[tern_columns[0]]]
                # bring a datapoint forward, if so specified
                z = 1
                if bring_forward:
                    if isinstance(bring_forward, str) and label == bring_forward:
                        z = 1.5
                    elif label in bring_forward:
                        z = 1.5
                tax.scatter(
                    data[tern_columns].values, label=label, c=color, zorder=z, **kwargs
                )

    # handle if data is not to be subdivided by color column
    else:
        tax.scatter(df[tern_columns].values, c=colors, **kwargs)


def tern_side_scale(
    tax,
    tickdict,
    ylabel,
    mid_ticklabel=False,
    bounds=(0, 100),
    xposition=0,
    innerticks=False,
    linewidth=1,
):
    """
    Sets left spine up as a vertical scale for the *tax* ternary plot.
    *tickdict* is a dictionary of tick labels and positions (on a scale
    of 0 to 1). If *mid_ticklabel=True*, ticklabels will be displayed
    between ticks, not on them. *ylabel* is the label of the scale,
    *bounds* is a 2-number tuple that specifies how high and low the
    axis extends, *xposition* specifies the x position where the scale
    will be moved.
    """
    ax = tax.get_axes()
    # handle inner ticks
    if innerticks:
        ha = "left"
    else:
        ha = None

    # remove other spines
    ax.axis("on")
    ax.set_xticks([])
    for direction in ["top", "right", "bottom"]:
        ax.spines[direction].set_visible(False)
    ax.spines["left"].set_linewidth(linewidth)

    # set spine position
    # find cosine of 30 degrees to get the length of the side scale
    top = np.cos(np.deg2rad(30)) * 100
    ax.spines["left"].set_bounds(bounds[0] * top / 100, bounds[1] * top / 100)
    ax.spines["left"].set_position(("data", xposition))

    # draw ticks
    ticks = [v * top / 100 for v in tickdict.values()]
    ax.set_yticks(ticks)

    # draw inbetween tick labels
    if mid_ticklabel:
        # remove major ticklabels
        ax.yaxis.set_major_formatter(NullFormatter())
        # get minor tick positions inbetween major ticks
        smallticks = []
        for i in range(len(ticks[:-1])):
            smallticks.append((ticks[i + 1] - ticks[i]) / 2 + ticks[i])
        smallticks.append((top - ticks[-1]) / 2 + ticks[-1])
        # draw hidden minor ticks
        ax.set_yticks(smallticks, minor=True)
        # write labels
        ax.set_yticklabels(list(tickdict.keys()), minor=True, ha=ha)
        ax.tick_params(axis="y", which="minor", length=0)
    else:
        # draw simple ticks
        ax.set_yticklabels(list(tickdict.keys()), ha=ha)

    # handle ticks on the inside of the scale
    if innerticks:
        ax.tick_params(axis="y", direction="in", pad=-10)

    # ax.set_yticklabels(list(dic.values()))
    ax.set_ylabel(ylabel, y=0.75)
