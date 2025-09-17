library(ggplot2)
library(readr)
library(dplyr)
#library(Xtable)
# Viewtable()
setwd("D:/University of Queensland/Data Science/Semester 1 2025/1_Extension of capstone project/PLOTS_829_ETS")
IDF <- read_csv("8ETS.csv")
#####################################################
IDF$ModelGroup <- ifelse(grepl("ETS", IDF$Forecast_Methods), "ETS")

for (i in 10:12) {
  p <- ggplot(IDF[IDF[1] == i,], aes(x = Holding_Costs, 
                                     y = Achieved_Service_Level,
                                     color = Forecast_Methods, 
                                     shape = as.factor(Target_Service_Level))) +
    geom_line(aes(group = interaction(Forecast_Methods)), size = 0.5) +
    geom_point(size = 2) +
    facet_wrap(~ Senario, scales = "fixed") +
    labs(x = "Holding Cost ($)", y = "Achieved Service Level (%)",
         color = "Forecast Method", shape = "Target Service Level (%)") +
    theme_bw(base_size = 11) +
    theme(strip.background = element_rect(fill = "gray85", color = "black"),
          strip.text = element_text(face = "bold"))
  
  ggsave(filename = paste0("ETS-level-", i, ".pdf"), plot = p, device = "pdf")#width = 8, height = 6,
}



for (i in 10:12) {
  df <- IDF[IDF[[1]] == i, ]
  
  df_labels <- df %>%
    group_by(Senario, ModelGroup) %>%
    summarise(Holding_Costs = max(Holding_Costs),
              Achieved_Service_Level = mean(Achieved_Service_Level),
              .groups = "drop")
  
  p <- ggplot(df,
              aes(x = Holding_Costs,
                  y = Achieved_Service_Level,
                  color = Forecast_Methods,
                  shape = Target_Service_Level,
                  group = interaction(Forecast_Methods, Senario))) +
    geom_line(size = 0.8) +
    geom_point(size = 2) +
    # 每个 Senario 一个标签
    geom_text(
      data = df_labels,
      aes(x = Holding_Costs,
          y = Achieved_Service_Level,
          label = Senario),
      inherit.aes = FALSE,
      hjust = -0.2,
      vjust = 0.5,
      show.legend = FALSE
    ) +
    facet_wrap(~ ModelGroup) +
    theme_bw(base_size = 12) +
    xlim(c(min(df$Holding_Costs), max(df$Holding_Costs) * 1.15))
  
  ggsave(filename = paste0("ETS-level-", i, ".pdf"),
         plot = p, device = "pdf")
}



######################################################## FOODS
IDF <- read_csv("721Base2IR_L1_Category.csv")
IDF <- IDF[IDF$Group=='FOODS',]
for (i in 10:12) {
  p <- ggplot(IDF[IDF[1] == i,], aes(x = Holding_Costs, 
                                     y = Achieved_Service_Level,
                                     color = Forecast_Methods, 
                                     shape = as.factor(Target_Service_Level))) +
    geom_line(aes(group = interaction(Forecast_Methods)), size = 0.5) +
    geom_point(size = 2) +
    facet_wrap(~ Senario, scales = "free") +
    labs(x = "Holding Cost ($)", y = "Achieved Service Level (%)",
         color = "Forecast Method", shape = "Target Service Level (%)") +
    theme_bw(base_size = 11) +
    theme(strip.background = element_rect(fill = "gray85", color = "black"),
          strip.text = element_text(face = "bold"))
  
  ggsave(filename = paste0("FOODS_LT1-level-", i, ".pdf"), plot = p, device = "pdf")#width = 8, height = 6,
}


######################################################## 'HOBBIES'
IDF <- read_csv("721Base2IR_L1_Category.csv")
IDF <- IDF[IDF$Group=='HOBBIES',]
for (i in 10:12) {
  p <- ggplot(IDF[IDF[1] == i,], aes(x = Holding_Costs, 
                                     y = Achieved_Service_Level,
                                     color = Forecast_Methods, 
                                     shape = as.factor(Target_Service_Level))) +
    geom_line(aes(group = interaction(Forecast_Methods)), size = 0.5) +
    geom_point(size = 2) +
    facet_wrap(~ Senario, scales = "free") +
    labs(x = "Holding Cost ($)", y = "Achieved Service Level (%)",
         color = "Forecast Method", shape = "Target Service Level (%)") +
    theme_bw(base_size = 11) +
    theme(strip.background = element_rect(fill = "gray85", color = "black"),
          strip.text = element_text(face = "bold"))
  
  ggsave(filename = paste0("HOOBIES_LT1-level-", i, ".pdf"), plot = p, device = "pdf")#width = 8, height = 6,
}





######################################################## HOUSEHOLD
IDF <- read_csv("721Base2IR_L1_Category.csv")
IDF <- IDF[IDF$Group=='HOUSEHOLD',]
for (i in 10:12) {
  p <- ggplot(IDF[IDF[1] == i,], aes(x = Holding_Costs, 
                                     y = Achieved_Service_Level,
                                     color = Forecast_Methods, 
                                     shape = as.factor(Target_Service_Level))) +
    geom_line(aes(group = interaction(Forecast_Methods)), size = 0.5) +
    geom_point(size = 2) +
    facet_wrap(~ Senario, scales = "free") +
    labs(x = "Holding Cost ($)", y = "Achieved Service Level (%)",
         color = "Forecast Method", shape = "Target Service Level (%)") +
    theme_bw(base_size = 11) +
    theme(strip.background = element_rect(fill = "gray85", color = "black"),
          strip.text = element_text(face = "bold"))
  
  ggsave(filename = paste0("HOUSEHOLD_LT1-level-", i, ".pdf"), plot = p, device = "pdf")#width = 8, height = 6,
}


########################################################### COSTS
IDF <- read_csv("ets_cost.csv")
for (i in 10:12) {
  p <- ggplot(IDF[IDF[1]==i,], aes(x = Holding_Costs+Backlogging_Costs, 
                                   y = Senario, #reorder(Forecast_Methods, 
                                   fill = factor(Forecast_Methods))) +
    #scale_fill_manual(values = c("darkgreen", "darkorange", "darkred")) +
    theme_bw(base_size = 11) +
    labs(x = "Total Cost ($)", y = "IR Methods", fill = "Forecast Methods")+
    theme(strip.background = element_rect(fill = "gray85", color = "black"),  
          strip.text = element_text(face = "bold"))+
    geom_bar(stat = "identity", position = "dodge") +
    facet_wrap(~ Target_Service_Level, scales = "free")
  
  ggsave(filename = paste0("ETS-level-costs-", i, ".pdf"), plot = p, device = "pdf")#width = 8, height = 6,
}

########################################################### MINTS
#IDF <- read_csv("721MinTs_IR_L1.csv")#721MinTs_IR_L1, 8_721Base2IR_L1_wls-var
for (i in 10:12) {
  p <- ggplot(IDF[IDF[1] == i,], aes(x = Holding_Costs, 
                                     y = Achieved_Service_Level,
                                     color = Forecast_Methods, 
                                     shape = as.factor(Target_Service_Level))) +
    geom_line(aes(group = interaction(Forecast_Methods)), size = 0.5) +
    geom_point(size = 2) +
    facet_wrap(~ Senario, scales = "fixed") +
    labs(x = "Holding Cost ($)", y = "Achieved Service Level (%)",
         color = "Forecast Method", shape = "Target Service Level (%)") +
    theme_bw(base_size = 11) +
    theme(strip.background = element_rect(fill = "gray85", color = "black"),
          strip.text = element_text(face = "bold"))
  
  ggsave(filename = paste0("MinTsLT1-level-", i, ".pdf"), plot = p, device = "pdf")#width = 8, height = 6,
}