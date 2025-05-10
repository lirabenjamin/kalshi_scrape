filter = dplyr::filter
data = read_csv("metaculus_open_questions.csv")

# mutate available for.
data = data %>% 
    mutate(available_for = case_when(
        is.na(actual_close_time) ~ difftime(ymd_hms("2025-05-09 15:15:13"), created_time, units = "days"),
        !is.na(actual_close_time) ~ difftime(actual_close_time, created_time, units = "days")
    )) %>% 
    mutate(main_category = str_split(category_descriptions, ";", simplify = TRUE)[,1])

data %>% filter(available_for < 0)

colnames(data)

a = data %>% 
    filter(available_for > 0) %>%
    ggplot(aes(x = available_for, y = forecasts_count, color= main_category))+ 
    geom_point() +
    theme(legend.position = "none") + 
    scale_y_log10(labels = scales::label_number(accuracy = 1, big.mark = ",")) + 
    labs(x = "Available for (days)", y = "Forecasts count", color = "First tagged category")

b = data %>% 
    mutate(forecasts_count = forecasts_count + 1) %>%
    filter(available_for > 0) %>%  
    lm(log(forecasts_count) ~ available_for + main_category, data = .)  %>% 
    emmeans::emmeans(~ main_category, type = "response")  %>%  
    as_tibble() %>%  
    ggplot(aes(x = reorder(main_category, response), y = response, fill = main_category)) +
    geom_col() +
    geom_errorbar(aes(ymin = response + SE, ymax = response - SE), width = 0.2) + 
    coord_flip() + 
    labs(subtitle = "Mean number of Forecasts", y = NULL)+
    theme(
        legend.position = 'none', 
        plot.subtitle = element_text(face = "bold", size = theme_get()$axis.title.y$size)
          )

ggpubr::ggarrange(a,b)


