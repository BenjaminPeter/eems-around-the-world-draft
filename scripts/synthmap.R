library(rworldmap)
library(sp)
library(gstat)
suppressPackageStartupMessages({
    library(ggplot2)
    library(magrittr)
})


spatial_subset_plot <- function(subset, PC, ...){
    l <- make_subset_data(subset)
    plot_factor_interpolation(l$data, l$boundary, PC, ...)
}

make_subset_data <- function(subset){
    data <- load_pca_data(sprintf("pca/flash_%s_dim20.pc", subset),
                      sprintf("subset/%s.fam", subset),
                      sprintf("subset/%s.indiv_meta", subset),
                      "pgs/gvar.pop_display")
    loc <- read.csv(sprintf("subset/%s.pop_geo", subset))
    data <- merge(data,loc)
    boundary <- read.table(sprintf("subset/%s.polygon", subset))
    names(boundary) <- c('x', 'y')


    d2 <- aggregate(data, list(data$abbrev),
                    function(x)ifelse(is.numeric(x), median(x),x[1]) )

    coordinates(d2) <- ~ longitude + latitude
    list(data=d2, boundary=boundary)
}


plot_factor_interpolation <- function(d2, boundary, PC, ...){
    k <- get_interpolation(d2, boundary, PC, ...)

    ggplot() %>%
        add_krig(k, boundary) %>%
        ggmap_plot() %>%
        add_original_points(d2, PC)
}


ggmap_plot <- function(G){
    source("scripts/ggeems/ggeems_main.R")
    m <- get_boundary_map()
    G = G + geom_path(data=m, aes(x=long, y=lat, group=group, width=.4),  color='#222222dd')
    #m <- getMap("low")
    #    G + geom_path(data = m, aes(x=long, y=lat, group = group),            
    #                         color = 'black') +                 
#        geom_polygon(data=boundary, aes(x=x, y=y), fill='red', alpha=.2)
}


add_krig <- function(G, k, boundary, column=3){
    kd <- as.data.frame(k)
    nvar <- as.name(names(kd)[column])
    G + geom_tile(data=kd, aes_(fill=as.name(nvar), x=~x1, y=~x2)) + 
                scale_fill_gradient(low="orange", high="blue") +
        scale_x_continuous(expand = c(0,0), limits=range(boundary[,1])) +
        scale_y_continuous(expand = c(0,0), limits=range(boundary[,2])) 
}

add_original_points <- function(G, data, PC="PC1"){
    G + geom_point(data=as.data.frame(data),
                   aes_(x=~longitude, y=~latitude, fill=as.name(PC)),
               size=2, shape=21, stroke=.5, colour="black") +
                scale_colour_gradient(low="orange", high="blue")
}


get_interpolation <- function(data, boundary, PC="PC1", n=5000, idp=5, maxdist=400,...){
    coordinates(boundary) <- ~ x + y 
    extrapolation_points <- spsample(Polygon(boundary), n=n, 'regular')

    #lzn.vgm <- variogram(as.name(PC)~1, data=data)                   
    #lzn.fit <- fit.variogram(lzn.vgm, model=vgm(model="Mat"))
    #k <- krige(PC2 ~ 1, data, extrapolation_points, model=lzn.fit) 
    res <-data.frame(coordinates(extrapolation_points),
          sapply(PC, function(P){
            fml <- as.formula(sprintf("%s ~ 1" ,P))
            x <- idw(fml, data, extrapolation_points, idp=idp, maxdist=maxdist,
                     ...) 
            names(x)[names(x) == 'var1.pred'] <- P
            as.data.frame(x)[,P]
           })
          )
    coordinates(res) <- ~ x1 + x2
    res
    }


