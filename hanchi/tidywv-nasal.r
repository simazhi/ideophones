getwd()



library(tidyverse)
library(tidytext)
library(widyr)



### `slide_windows`
slide_windows <- function(tbl, doc_var, window_size) {
  # each word gets a skipgram (window_size words) starting on the first
  # e.g. skipgram 1 starts on word 1, skipgram 2 starts on word 2
  
  each_total <- tbl %>% 
    group_by(!!doc_var) %>% 
    mutate(doc_total = n(),
           each_total = pmin(doc_total, window_size, na.rm = TRUE)) %>%
    pull(each_total)
  
  rle_each <- rle(each_total)
  counts <- rle_each[["lengths"]]
  counts[rle_each$values != window_size] <- 1
  
  # each word get a skipgram window, starting on the first
  # account for documents shorter than window
  id_counts <- rep(rle_each$values, counts)
  window_id <- rep(seq_along(id_counts), id_counts)
  
  
  # within each skipgram, there are window_size many offsets
  indexer <- (seq_along(rle_each[["values"]]) - 1) %>%
    map2(rle_each[["values"]] - 1,
         ~ seq.int(.x, .x + .y)) %>% 
    map2(counts, ~ rep(.x, .y)) %>%
    flatten_int() +
    window_id
  
  tbl[indexer, ] %>%
    bind_cols(data_frame(window_id)) %>%
    group_by(window_id) %>%
    filter(n_distinct(!!doc_var) == 1) %>%
    ungroup
}


### `tidy_pmi`
tidy_pmi <- function(dataframe){
  dataframe %>%
    unnest_tokens(word, text, token = "regex", pattern = " ") %>%
    add_count(word) %>%
    #filter(n >= 10) %>% 
    select(-n) %>%
    slide_windows(quo(postID), 8) %>%
    pairwise_pmi(word, window_id)
}

### `checking_tidy_pmi `
checking_tidy_pmi <- function(tidydataframe, column, target){
  tidydataframe %>%
    filter(column %in% target) #target needs to be character
}

### `tidy_word_vectors`
tidy_word_vectors <- function(tidydataframe){
  tidydataframe %>%
    widely_svd(item1, item2, pmi, nv = 256, maxit = 1000)
}

### `nearest_synonyms`
nearest_synonyms <- function(df, token) {
  df %>%
    widely(~ . %*% (.[token, ]), 
           sort = TRUE,
           maximum_size = NULL)(item1, dimension, value) %>% #max size = null will prevent stuff
    select(-item2)
}

### `result_table`
resulttable <- function(textobject){
  
  print(textobject)
  
  TARGETbare <- textobject %>%
    str_extract(".._") %>%
    str_replace("_", "")  
  
  suffix <- str_extract(textobject, "_[a-z]*")
  
  text_df <- textobject %>% 
    read_lines() %>%
    unlist() %>%
    data_frame(text = .) %>%
    distinct() %>% 
    mutate(postID = row_number())
  
  results <- text_df %>%
    tidy_pmi() %>%
    tidy_word_vectors() %>%
    nearest_synonyms(TARGETbare) %>%
    top_n(1000) #before top 300, but maybe not enough?
  
  path <- sprintf("./diachronicnasal/%s%s.csv", TARGETbare, suffix)
  
  if (!file.exists(path)){
    dir.create("./diachronicnasal")
    file.create(path)
  }
  
  write_csv(results, path, append = F)
  
  Sys.sleep(5)
}


### DATA 

# find files
files <- list.files(path = "./segmentednasal",
                    #pattern = sprintf('*%s.txt', "_"), 
                    full.names = TRUE
                    )
files

# target
#TARGETbare <- "灼灼"
#TARGET <- sprintf("%s_.*", TARGETbare)


### FUNCTION CALL
map(files, resulttable)


