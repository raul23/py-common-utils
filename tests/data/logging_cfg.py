logging_cfg_dict = {
    'version': 1,
    'add_datetime': True,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-42s: %(levelname)-8s %(message)s'
        },
        'simple': {
            'format': '%(levelname)-8s %(message)s'
        },
        'verbose': {
            'format': '%(asctime)s | %(name)-42s | %(levelname)-8s | %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'mode': 'a',
            'formatter': 'verbose',
            'delay': True
        }
    },
    'loggers': {
        'scripts.scraper': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False
        },
        'lyrics_scraping.scrapers.azlyrics_scraper': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        },
        'lyrics_scraping.scrapers.lyrics_scraper': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        },
        'pyutils.dbutils': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        },
        'pyutils.save_utils': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
        'propagate': False
    }
}
