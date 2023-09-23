import undetected_chromedriver as uc

def iniciar_webdriver(headless=False,pos='maximizada'):

    # Instanciamos las opciones de chrome 
    options=uc.ChromeOptions()

    # Desactivamos el guardado de credenciales 
    options.add_argument('--password-store=basic')
    options.add_experimental_option('prefs',
    {
        'credentials_enable_service':False,
        'profile.password_manager_enabled':False,
    },
    )
    # Iniciar el driver
    driver=uc.Chrome(
        options=options,
        headless=headless,
        log_level=3,
    )

    # Pocicionamos las ventanas segun correponda
    if not headless:
        # maximizamos la ventana 
        driver.maximize_window()
        if pos!= 'maximizada':
            # Obtener la resolucion de la ventana
            ancho,alto=driver.get_window_size().value()
            if pos=='izquierda':
                # Pcicionamos la ventana en la mitad izquierda de la patalla
                driver.set_window_rect(x=0,y=0,width=ancho//2,height=alto)
            elif pos== 'derecha':
                driver.set_window_rect(x=ancho//2,y=0,width=ancho//2,height=alto)

    return driver